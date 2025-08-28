----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/07/2025 03:26:24 PM
-- Design Name: 
-- Module Name: puf_starter - Behavioral
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

entity puf_starter is
    port (
        clk:      in  std_logic;
        pulse:    in  std_logic;
        data_out: out std_logic_vector(1 downto 0)
    );
end puf_starter;

architecture Behavioral of puf_starter is
    attribute DONT_TOUCH: boolean;
    
    component FDRE 
        port (
            Q:  out std_logic;
            C:  in  std_logic;
            CE: in  std_logic;
            R:  in  std_logic;
            D:  in  std_logic
        );
    end component;
    
    attribute DONT_TOUCH of activator0: label is true;
    attribute DONT_TOUCH of activator1: label is true;
    
begin
    
    activator0: FDRE port map (
        Q => data_out(0),
        C => clk,
        CE => '1',
        D => pulse,
        R => '0'
    );
    
    activator1: FDRE port map (
        Q => data_out(1),
        C => clk,
        CE => '1',
        D => pulse,
        R => '0'
    );

end Behavioral;
