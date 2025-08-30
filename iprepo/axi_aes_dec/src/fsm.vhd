----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/31/2025 12:06:26 AM
-- Design Name: 
-- Module Name: fsm - Behavioral
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

entity fsm is
    port (
		clk : in std_logic;
		trigger: in std_logic;
		key : in std_logic_vector(127 downto 0);
		ciphertext : in std_logic_vector(127 downto 0);
		plaintext : out std_logic_vector(127 downto 0);
		busy : out std_logic		
	);
end fsm;

architecture Behavioral of fsm is
    attribute MARK_DEBUG: boolean;

    type state_t is (IDLE, EXEC, DONE);
    signal curstate: state_t := IDLE;
    
    signal busy_reg: std_logic := '0';
    signal plain_reg: std_logic_vector(127 downto 0);
    
    signal dec_done: std_logic;
    signal dec_reset: std_logic := '0';
    signal dec_result: std_logic_vector(127 downto 0);
    
    attribute MARK_DEBUG of curstate, dec_done, dec_reset: signal is true;
begin
    busy <= busy_reg;
    plaintext <= plain_reg;
    
    -- im tired, just gonna put everything in a process
    process (clk) begin
    if rising_edge(clk) then
        
        if curstate = IDLE then
            if trigger = '1' then
                busy_reg <= '1';
                dec_reset <= '1';
                curstate <= EXEC;
            end if;
        elsif curstate = EXEC then
            if dec_done = '1' then
                curstate <= DONE;
                plain_reg <= dec_result;
                dec_reset <= '0';
                busy_reg <= '0';
            end if;
        elsif curstate = DONE then
            if trigger = '0' then
                curstate <= IDLE;
            end if;
        end if;
    end if;    
    end process;
    
    AES_ENC: entity work.aes_dec
    port map (
        clk => clk,
        rst => dec_reset,
        dec_key => key,
        ciphertext => ciphertext,
        plaintext => dec_result,
        done => dec_done
    );

end Behavioral;
