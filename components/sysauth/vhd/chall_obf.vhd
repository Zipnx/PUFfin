----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/15/2025 12:47:27 PM
-- Design Name: 
-- Module Name: chall_obf - Behavioral
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

entity chall_obf is
    port (
        iObfuscate: in  std_logic_vector(31 downto 0);
        iChallenge: in  std_logic_vector(31 downto 0);
        oChallenge: out std_logic_vector(31 downto 0)
    );
end chall_obf;

-- This entity exists purely so that i can experiment with some different
-- obfuscation functions

architecture barebone of chall_obf is
begin
    oChallenge <= iObfuscate xor iChallenge;
end barebone;
