----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 20.08.2025 15:21:22
-- Design Name: 
-- Module Name: compressor - Behavioral
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

entity ent_compressor is
    Port ( code_in : in STD_LOGIC_VECTOR (48 downto 0);
           code_out : out STD_LOGIC_VECTOR (48 downto 0));
end ent_compressor;

architecture Behavioral of ent_compressor is

begin
process (code_in)
begin 
code_out <= code_in ;
code_out(0)  <= code_in(0)  xor code_in(5);
code_out(2)  <= code_in(2)  xor code_in(6);
code_out(3)  <= code_in(3)  xor code_in(8);
code_out(4)  <= code_in(4)  xor code_in(9);
code_out(7)  <= code_in(7)  xor code_in(11);
code_out(10) <= code_in(10) xor code_in(14);
code_out(12) <= code_in(12) xor code_in(15);
code_out(13) <= code_in(13) xor code_in(16);
code_out(20) <= code_in(20) xor code_in(21);
code_out(24) <= code_in(24) xor code_in(26);
code_out(28) <= code_in(28) xor code_in(29);
code_out(32) <= code_in(32) xor code_in(33);
code_out(35) <= code_in(35) xor code_in(37);
code_out(36) <= code_in(36) xor code_in(38);

end process;

end Behavioral;
