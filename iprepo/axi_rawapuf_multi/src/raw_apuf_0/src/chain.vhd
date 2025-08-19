----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/08/2025 04:36:15 PM
-- Design Name: 
-- Module Name: chain - Behavioral
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
library UNISIM;
use UNISIM.VComponents.all;

entity chain is
    generic (
        CHALL_BITS: integer := 4
    );
    port (
        challenge:          in  std_logic_vector(CHALL_BITS - 1 downto 0);
        up_in, down_in:     in  std_logic;
        up_out, down_out:   out std_logic
    );
end chain;

architecture Behavioral of chain is
    attribute DONT_TOUCH: boolean;
    
    signal chain_up, chain_down: std_logic_vector(CHALL_BITS downto 0);
    
    attribute DONT_TOUCH of CHAIN_GEN_UP: label is true;
    attribute DONT_TOUCH of CHAIN_GEN_DOWN: label is true;
    
    attribute DONT_TOUCH of chain_up: signal is true;
    attribute DONT_TOUCH of chain_down: signal is true;
begin
    
    chain_up(0)   <= up_in;
    chain_down(0) <= down_in;
    
    up_out   <= chain_up(CHALL_BITS);
    down_out <= chain_down(CHALL_BITS);
    
    -- setup the upper
    CHAIN_GEN_UP: for i in 1 to CHALL_BITS generate
        
        MUX_INST: LUT3
        generic map (INIT => "11001010") -- original design had an error here
        port map (
            O  => chain_up(i),
            I0 => chain_up(i - 1),
            I1 => chain_down(i - 1),
            I2 => challenge(i - 1)
        );
    end generate; 
    
    -- now the lower
    CHAIN_GEN_DOWN: for i in 1 to CHALL_BITS generate
        
        MUX_INST: LUT3
        generic map (INIT => "11001010")
        port map (
            O  => chain_down(i),
            I0 => chain_down(i - 1),
            I1 => chain_up(i - 1),
            I2 => challenge(i - 1)
        );
        
    end generate; 
    
    
    
end Behavioral;
