

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity RO_EdgeCounter is
  generic (
    WIDTH : integer := 24
  );
  port (
    rstn     : in  std_logic;                          -- Active-low reset
    ro_clk   : in  std_logic;                          -- RO signal used as clock
    count    : out std_logic_vector(WIDTH-1 downto 0)  -- Output count
  );
end entity;

architecture Behavioral of RO_EdgeCounter is
  signal counter : unsigned(WIDTH-1 downto 0) := (others => '0');
begin
  process(ro_clk, rstn)
  begin
    if rstn = '1' then
      counter <= (others => '0');
    elsif rising_edge(ro_clk) then
      counter <= counter + 1;
    end if;
  end process;

  count <= std_logic_vector(counter);
end architecture;
