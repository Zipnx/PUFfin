----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/12/2025 09:06:31 PM
-- Design Name: 
-- Module Name: arbiter_xorstyle - Behavioral
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

entity arbiter_xorstyle is
    port (
        clk, rst: in std_logic;
        data: in  std_logic_vector(1 downto 0);
        resp: out std_logic
    );
end arbiter_xorstyle;

architecture Behavioral of arbiter_xorstyle is
    attribute DONT_TOUCH: boolean;
    
    signal xor_result: std_logic;
    
    attribute DONT_TOUCH of XOR_INST: label is true;
    attribute DONT_TOUCH of DFF_INST: label is true;
begin
    XOR_INST: LUT2 generic map (INIT => X"0110")
    port map (
        O  => xor_result,
        I0 => data(0),
        I1 => data(1) 
    );
    
    DFF_INST: FDRE port map (
        Q => resp,
        C => clk,
        CE => '1',
        R => rst,
        D => xor_result
    );
    
end Behavioral;
