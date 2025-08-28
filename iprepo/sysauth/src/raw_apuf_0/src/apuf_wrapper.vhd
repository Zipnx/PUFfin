----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/20/2025 06:46:43 PM
-- Design Name: 
-- Module Name: apuf_wrapper - Behavioral
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity apuf_wrapper is
    generic (
        BIT_WIDTH:     integer := 32;
        CHALL_BITS:    integer := 32;
        INTCONFIG:     std_logic_vector := "011011"
    );
    port (
        clk:        in  std_logic;
        trigger:    in  std_logic;
        challenge:  in  std_logic_vector(CHALL_BITS - 1 downto 0);
        busy:       out std_logic;
        response:   out std_logic_vector(BIT_WIDTH - 1 downto 0)
    );
end apuf_wrapper;

architecture Behavioral of apuf_wrapper is
    
    type state_t is (IDLE, EXEC, DONE);
    
    
    attribute MARK_DEBUG: boolean;
    attribute MARK_DEBUG of challenge: signal is true;
    
    signal current_state: state_t := IDLE;
begin
    
    APUF_INST: entity work.nxn_apuf
    generic map (
        BIT_WIDTH => BIT_WIDTH, CHALL_BITS => CHALL_BITS,
        INTCONFIG => INTCONFIG
    )
    port map (
        CLK => clk, IPULSE => trigger,
        CHALLENGE => challenge,
        RESPONSE  => response
    );
    
    STATE_PROC: process (clk) begin
        
        if rising_edge(clk) then
            
            if current_state = IDLE then
                if trigger = '1' then
                    current_state <= EXEC;
                    busy <= '1';
                else
                    busy <= '0';
                end if;
            elsif current_state = EXEC then
                current_state <= DONE;
                busy <= '0';
            
            elsif current_state = DONE then    
                if trigger = '0' then
                    current_state <= IDLE;
                end if;
            end if;
            
        end if;
        
    end process;
    
end Behavioral;
