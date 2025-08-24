----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05.07.2025 12:41:36
-- Design Name: 
-- Module Name: TOP - Behavioral
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

entity TOP is
port (
    clk   : in std_logic;
    reset : in std_logic ;       -- Asynchronous reset for the counter
    en   : in  std_logic;                      -- Enable all ROs
    sel  : in  std_logic_vector(2 downto 0);   -- Select RO output
    count : out std_logic_vector(23 downto 0)
 
  );
end TOP;

architecture Behavioral of TOP is
    attribute MARK_DEBUG: boolean;
    attribute MARK_DEBUG of count, en: signal is true;

    -- batch of 8 ring oscillators 
    component batch8
        port (
          clk  : in  std_logic;
          en   : in  std_logic;
          sel  : in  std_logic_vector(2 downto 0);
          o    : out std_logic
        );
    end component ;
    -- counter 
    component RO_EdgeCounter
        generic (WIDTH : integer := 24);
        port (
          rstn : std_logic ;
          ro_clk   : in  std_logic;
          count    : out std_logic_vector(WIDTH-1 downto 0)
        );
    end component;
    
    
    signal ro_signals : std_logic_vector(7 downto 0);
    signal selected_ro : std_logic;
begin

  ro_batch_inst : batch8
    port map (
      clk => clk,
      en  => en,
      sel => sel,
      o   => selected_ro
    );


  counter_inst : RO_EdgeCounter
    generic map (WIDTH => 24)
    port map (
      rstn => reset,
      ro_clk  => selected_ro,
      count   => count
    );
    
end Behavioral;
