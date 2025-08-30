----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/30/2025 10:43:15 PM
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
		plaintext : in std_logic_vector(127 downto 0);
		ciphertext : out std_logic_vector(127 downto 0);
		busy : out std_logic		
	);
end fsm;

architecture Behavioral of fsm is
    attribute MARK_DEBUG: boolean;

    type state_t is (IDLE, EXEC, DONE);
    signal curstate: state_t := IDLE;
    
    signal busy_reg: std_logic := '0';
    signal ciph_reg: std_logic_vector(127 downto 0);
    
    signal enc_done: std_logic;
    signal enc_reset: std_logic := '0';
    signal enc_result: std_logic_vector(127 downto 0);
    
    attribute MARK_DEBUG of curstate, enc_done, enc_reset: signal is true;
begin
    busy <= busy_reg;
    ciphertext <= ciph_reg;
    
    -- im tired, just gonna put everything in a process
    process (clk) begin
    if rising_edge(clk) then
        
        if curstate = IDLE then
            if trigger = '1' then
                busy_reg <= '1';
                enc_reset <= '1';
                curstate <= EXEC;
            end if;
        elsif curstate = EXEC then
            if enc_done = '1' then
                curstate <= DONE;
                ciph_reg <= enc_result;
                enc_reset <= '0';
                busy_reg <= '0';
            end if;
        elsif curstate = DONE then
            if trigger = '0' then
                curstate <= IDLE;
            end if;
        end if;
    end if;    
    end process;
    
    AES_ENC: entity work.aes_enc
    port map (
        clk => clk,
        rst => enc_reset,
        key => key,
        plaintext => plaintext,
        ciphertext => enc_result,
        done => enc_done
    );

end Behavioral;
