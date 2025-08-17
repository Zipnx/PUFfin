----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/04/2025 08:18:09 PM
-- Design Name: 
-- Module Name: majpoll - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
--use work.ext_types.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity majpoll is
    generic (
        BITLENGTH: integer := 32;
        REGISTER_COUNT: integer := 3
    );
    port (
        iClk, iRead, iTrigger, iRst: in std_logic;
        iData: in  std_logic_vector(BITLENGTH - 1 downto 0);
        oData: out std_logic_vector(BITLENGTH - 1 downto 0)
    );
end majpoll;

architecture dynamic of majpoll is
    type u64_arr_t is array (natural range <>) of std_logic_vector(BITLENGTH - 1 downto 0);
    
    signal read_enable_reg, trigger_reg: std_logic;
    
    signal pipeline: u64_arr_t(0 to REGISTER_COUNT - 1);
    
begin
    
    LD_PIPELINE: process (iClk, iRst)
    begin 
        if iRst = '1' then
            -- Empty the pipeline
            for i in 0 to REGISTER_COUNT - 1 loop
                pipeline(i) <= (others => '0');
            end loop;
        elsif rising_edge(iClk) then
            if iRead = '1' then
                for i in 1 to REGISTER_COUNT - 1 loop
                    pipeline(i) <= pipeline(i - 1);
                end loop;
                
                pipeline(0) <= iData; -- Hope vivado infers the right structure from all this...
            end if;
        end if;
    end process;
    
    EXECUTE: process (iClk) 
        variable counter: integer := 0;
    begin
        for i in BITLENGTH - 1 downto 0 loop
            counter := 0;
            
            for j in 0 to REGISTER_COUNT - 1 loop
                if pipeline(j)(i) = '1' then 
                    counter := counter + 1; 
                end if;
            end loop;
            
            if counter >= BITLENGTH / 2 then 
                oData(i) <= '1';
            else
                oData(i) <= '0';
            end if;
        
        end loop;
    end process;

end dynamic;

-- NOTE:
-- Primarily made this because the dynamic version broke out of nowhere and im too lazy to debug it
-- also for some reason dynamic's synthesis doesnt work, as in 0 LUTs and 0 FFs, honestly, no idea
-- better leave it for dead, gonna be 32 bit with 3 registers either way
architecture hardcode of majpoll is
    attribute MARK_DEBUG: boolean;
    
    signal A, B, C: std_logic_vector(BITLENGTH - 1 downto 0) := (others => '0');
    attribute MARK_DEBUG of iData, oData: signal is true;
    attribute MARK_DEBUG of iRead, iRst: signal is true;
    attribute MARK_DEBUG of A,B,C: signal is true;
begin
    
    PIPELINE: process (iClk, iRst)
    begin
        
        if iRst = '1' then
            A <= (others => '0');
            B <= (others => '0');
            C <= (others => '0');
        
        elsif rising_edge(iClk) and iRead = '1' then
            C <= B;
            B <= A;
            A <= iData;
        end if;
        
    end process;
    
    EXECUTE: process (iClk)
        variable result: std_logic_vector(BITLENGTH - 1 downto 0);
    begin
        if rising_edge(iClk) and iTrigger = '1' then
            for i in BITLENGTH - 1 downto 0 loop
                result(i) := (A(i) and B(i)) or
                             (A(i) and C(i)) or
                             (B(i) and C(i));
            end loop;
        end if;
        
        oData <= result;
    end process;
    
end hardcode;
