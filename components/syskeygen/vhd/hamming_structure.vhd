----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/30/2025 03:29:57 PM
-- Design Name: 
-- Module Name: hamming_structure - Behavioral
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity hamming_structure is
    generic (
        PARITY0: std_logic_vector(27 downto 0) := (others => '0');
        PARITY1: std_logic_vector(27 downto 0) := (others => '0');
        PARITY2: std_logic_vector(27 downto 0) := (others => '0')
    );
    port (
        iData:      in  std_logic_vector(48 downto 0);
        iSelect:    in  std_logic_vector(2 downto 0);
        oData:      out std_logic_vector(76 downto 0)
    );
end hamming_structure;

architecture Behavioral of hamming_structure is

begin
    
    CONSTRUCT: process (iData)
        variable parity: std_logic_vector(27 downto 0);
        variable block_data: std_logic_vector(6 downto 0);
        variable block_parity: std_logic_vector(3 downto 0);
    begin 
        
        if iSelect = "000" then
            parity := PARITY0;
        elsif iSelect = "001" then
            parity := PARITY1;
        else
            parity := PARITY2;
        end if;
        
        for i in 0 to 6 loop
            block_data      := iData((i + 1)*7 - 1 downto i*7);
            block_parity    := parity((i + 1)*4 - 1 downto i * 4);
            
            oData(i*11)     <= block_parity(0);
            oData(i*11 + 1) <= block_parity(1);
            
            oData(i*11 + 2) <= block_data(0);
            
            oData(i*11 + 3) <= block_parity(2);
            
            oData(i*11 + 4) <= block_data(1);
            oData(i*11 + 5) <= block_data(2);
            oData(i*11 + 6) <= block_data(3);
            
            oData(i*11 + 7) <= block_parity(3);
            
            oData(i*11 + 8) <= block_data(4);
            oData(i*11 + 9) <= block_data(5);
            oData(i*11 + 10) <= block_data(6);
           
        end loop;
        
    end process;

end Behavioral;
