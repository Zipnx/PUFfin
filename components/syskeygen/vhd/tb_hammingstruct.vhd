----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/30/2025 04:01:25 PM
-- Design Name: 
-- Module Name: tb_hammingstruct - Behavioral
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

entity tb_hammingstruct is
--  Port ( );
end tb_hammingstruct;

architecture Behavioral of tb_hammingstruct is
    signal iData: std_logic_vector(48 downto 0);
    signal oData: std_logic_vector(76 downto 0);
    signal iSel:  std_logic_vector(2 downto 0);
begin
    
    dut: entity work.hamming_structure
    generic map (
        PARITY0 => "0000101100001000011111110111",
        PARITY1 => "0000101100001000011111110111",
        PARITY2 => "0000101100001000011111110111"
    )
    port map (
        iData => iData, oData => oData, iSelect => iSel
    );
    
    process begin
        iData <= "0000000011111000111000111000111000111000111000111";
        iSel  <= "000";
        
        wait;
    end process;
    
end Behavioral;
