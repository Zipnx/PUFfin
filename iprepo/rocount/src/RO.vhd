library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
library UNISIM;
use UNISIM.VComponents.all;

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

library UNISIM;
use UNISIM.VComponents.all;

entity RO is
  port (
    clk : in  std_logic;
    en  : in  std_logic;
    o   : out std_logic
  );
end entity;

architecture Behavioral of RO is
  signal t0, t1, t2, t3, t4, t5, t6, t7, t8, t9 : std_logic;
  signal c : std_logic_vector(9 downto 0) := (others => '0');
  
  signal enable_int: std_logic;

  attribute KEEP       : string;
  attribute DONT_TOUCH : string;
  attribute KEEP       of t0, t1, t2, t3, t4, t5, t6, t7, t8, t9 : signal is "true";
  attribute DONT_TOUCH of t0, t1, t2, t3, t4, t5, t6, t7, t8, t9 : signal is "true";
begin
  
  enabler: FDRE port map (
    Q  => enable_int,
    D  => en,
    CE => '1',
    C  => clk,
    R  => '0'
  );
  
  -- NAND gate: t0 = NAND(en, t9)
  LUT6_L_NAND0 : LUT6_L
    generic map (
      INIT => X"8888888888888888"
    )
    port map (
      I0 => enable_int,
      I1 => t9,
      I2 => c(0),
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t0
    );

  -- Inverter 1
  LUT6_L_INV0 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t0,
      I1 => c(1),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t1
    );

  -- Inverter 2
  LUT6_L_INV1 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t1,
      I1 => c(2),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t2
    );

  -- Inverter 3
  LUT6_L_INV2 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t2,
      I1 => c(3),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t3
    );

  -- Inverter 4
  LUT6_L_INV3 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t3,
      I1 => c(4),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t4
    );

  -- Inverter 5
  LUT6_L_INV4 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t4,
      I1 => c(5),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t5
    );

  -- Inverter 6
  LUT6_L_INV5 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t5,
      I1 => c(6),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t6
    );

  -- Inverter 7
  LUT6_L_INV6 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t6,
      I1 => c(7),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t7
    );

  -- Inverter 8
  LUT6_L_INV7 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t7,
      I1 => c(8),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t8
    );

  -- Inverter 9 (feedback)
  LUT6_L_INV8 : LUT6_L
    generic map (
      INIT => X"5555555555555555"
    )
    port map (
      I0 => t8,
      I1 => c(9),
      I2 => '0',
      I3 => '0',
      I4 => '0',
      I5 => '0',
      LO => t9
    );

  -- Output
  o <= t9;

end architecture;
