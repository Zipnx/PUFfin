----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07.07.2025 11:33:45
-- Design Name: 
-- Module Name: batch8 - Behavioral
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

entity batch8 is
 port (
    clk  : in  std_logic;
    en   : in  std_logic;
    sel  : in  std_logic_vector(2 downto 0);  -- select which RO to output
    o    : out std_logic
  );
end batch8;

architecture Behavioral of batch8 is
component RO is
    port (
      clk : in  std_logic;
      en  : in  std_logic;
      o   : out std_logic
    );
  end component;
  
signal ro_outputs : std_logic_vector(2 downto 0);
begin

gen_ro: for i in 0 to 2 generate
    ro_inst: RO
      port map (
        clk => clk,
        en => en,
        o  => ro_outputs(i)
      );
end generate;
with sel select
    o <= ro_outputs(0) when "0000",
         ro_outputs(1) when "0001",
         ro_outputs(2) when "0010",
         '0'            when others;


end Behavioral;
