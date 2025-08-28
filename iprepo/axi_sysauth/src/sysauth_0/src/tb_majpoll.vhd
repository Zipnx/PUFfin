----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/04/2025 08:37:26 PM
-- Design Name: 
-- Module Name: tb_majpoll - Behavioral
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

entity tb_majpoll is
--  Port ( );
end tb_majpoll;

architecture Behavioral of tb_majpoll is
    signal clk, read, trig, rst: std_logic := '0';
    signal input, output: std_logic_vector(3 downto 0) := (others => '0');
begin
    clk <= not clk after 10 ns;
    
    dut: entity work.majpoll(dynamic)
    generic map (BITLENGTH => 4, REGISTER_COUNT => 3)
    port map (
        iClk => clk, iRead => read, iTrigger => trig, iRst => rst,
        iData => input,
        oData => output
    );
    
    process begin
        
        
        read <= '1';
        input <= "1011";
        wait until rising_edge(clk);
        input <= "1000";
        wait until rising_edge(clk);
        input <= "1001";
        wait until rising_edge(clk); -- this is done, because if done on the same CC, there can be a timing issue
        trig <= '1';
        read <= '0';
        wait until rising_edge(clk);
        trig <= '0';
        input <= "0000";
        wait until rising_edge(clk);
        wait for 100 ns;
        trig <= '0';
        
        wait;
    end process;

end Behavioral;






















