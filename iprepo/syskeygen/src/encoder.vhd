
-- Lehme Encoder for 16 inputs
-- Computes Lehmer code, converts to Gray, concatenates


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity encoder is
  Port (
    C1, C2, C3, C4, C5, C6, C7, C8,
    C9, C10, C11, C12, C13, C14, C15, C16 : in unsigned(23 downto 0);
    code_out : out std_logic_vector(48 downto 0)  -- 49 bits
  );
end encoder;

architecture Behavioral of encoder is

  -- Gray code conversion
  function bin_to_gray(bin_val : unsigned) return unsigned is
  begin
    return bin_val xor (bin_val srl 1);
  end function;

  -- Gray versions of Lehmer coefficients
  signal G1  : unsigned(0 downto 0);
  signal G2  : unsigned(1 downto 0);
  signal G3  : unsigned(1 downto 0);
  signal G4  : unsigned(2 downto 0);
  signal G5  : unsigned(2 downto 0);
  signal G6  : unsigned(2 downto 0);
  signal G7  : unsigned(2 downto 0);
  signal G8  : unsigned(3 downto 0);
  signal G9  : unsigned(3 downto 0);
  signal G10 : unsigned(3 downto 0);
  signal G11 : unsigned(3 downto 0);
  signal G12 : unsigned(3 downto 0);
  signal G13 : unsigned(3 downto 0);
  signal G14 : unsigned(3 downto 0);
  signal G15 : unsigned(3 downto 0);
type count_array is array(1 to 16) of unsigned(23 downto 0);
begin

process(C1, C2, C3, C4, C5, C6, C7, C8,
        C9, C10, C11, C12, C13, C14, C15, C16)
    variable cnt : integer;
    variable vL1  : unsigned(0 downto 0);
    variable vL2  : unsigned(1 downto 0);
    variable vL3  : unsigned(1 downto 0);
    variable vL4  : unsigned(2 downto 0);
    variable vL5  : unsigned(2 downto 0);
    variable vL6  : unsigned(2 downto 0);
    variable vL7  : unsigned(2 downto 0);
    variable vL8  : unsigned(3 downto 0);
    variable vL9  : unsigned(3 downto 0);
    variable vL10 : unsigned(3 downto 0);
    variable vL11 : unsigned(3 downto 0);
    variable vL12 : unsigned(3 downto 0);
    variable vL13 : unsigned(3 downto 0);
    variable vL14 : unsigned(3 downto 0);
    variable vL15 : unsigned(3 downto 0);
    variable Ci : unsigned(23 downto 0);
    variable C   : count_array;
begin
    -- put inputs into array for easier loops
    C(1) := C1;  C(2) := C2;  C(3) := C3;  C(4) := C4;
    C(5) := C5;  C(6) := C6;  C(7) := C7;  C(8) := C8;
    C(9) := C9;  C(10) := C10; C(11) := C11; C(12) := C12;
    C(13) := C13; C(14) := C14; C(15) := C15; C(16) := C16;

    -- Compute Lehmer coefficients (1 to 15)
    -- L1
    cnt := 0;
    if C(2) > C(1) then cnt := cnt + 1; end if;
    vL1 := to_unsigned(cnt, vL1'length);

    -- L2
    cnt := 0;
    for j in 1 to 2 loop
      if C(3) > C(j) then cnt := cnt + 1; end if;
    end loop;
    vL2 := to_unsigned(cnt, vL2'length);

    -- L3
    cnt := 0;
    for j in 1 to 3 loop
      if C(4) > C(j) then cnt := cnt + 1; end if;
    end loop;
    vL3 := to_unsigned(cnt, vL3'length);

    -- L4..L15
    cnt := 0;
    for j in 1 to 4 loop
      if C(5) > C(j) then cnt := cnt + 1; end if;
    end loop;
    vL4 := to_unsigned(cnt, vL4'length);

    for i in 5 to 15 loop
      cnt := 0;
      for j in 1 to i loop
        if C(i+1) > C(j) then cnt := cnt + 1; end if;
      end loop;
      case i is
        when 5  => vL5  := to_unsigned(cnt, vL5'length);
        when 6  => vL6  := to_unsigned(cnt, vL6'length);
        when 7  => vL7  := to_unsigned(cnt, vL7'length);
        when 8  => vL8  := to_unsigned(cnt, vL8'length);
        when 9  => vL9  := to_unsigned(cnt, vL9'length);
        when 10 => vL10 := to_unsigned(cnt, vL10'length);
        when 11 => vL11 := to_unsigned(cnt, vL11'length);
        when 12 => vL12 := to_unsigned(cnt, vL12'length);
        when 13 => vL13 := to_unsigned(cnt, vL13'length);
        when 14 => vL14 := to_unsigned(cnt, vL14'length);
        when 15 => vL15 := to_unsigned(cnt, vL15'length);
        when others => null;
      end case;
    end loop;

    -- Convert to Gray
    G1  <= bin_to_gray(vL1);
    G2  <= bin_to_gray(vL2);
    G3  <= bin_to_gray(vL3);
    G4  <= bin_to_gray(vL4);
    G5  <= bin_to_gray(vL5);
    G6  <= bin_to_gray(vL6);
    G7  <= bin_to_gray(vL7);
    G8  <= bin_to_gray(vL8);
    G9  <= bin_to_gray(vL9);
    G10 <= bin_to_gray(vL10);
    G11 <= bin_to_gray(vL11);
    G12 <= bin_to_gray(vL12);
    G13 <= bin_to_gray(vL13);
    G14 <= bin_to_gray(vL14);
    G15 <= bin_to_gray(vL15);

    -- Concatenate (MSB = G1, LSB = G15)
   -- code_out <= std_logic_vector(
               --   G1 & G2 & G3 & G4 & G5 & G6 & G7 & G8 & G9 & G10 & G11 & G12 & G13 & G14 & G15
              --  );

end process;
code_out <= std_logic_vector(G1)  &
            std_logic_vector(G2)  &
            std_logic_vector(G3)  &
            std_logic_vector(G4)  &
            std_logic_vector(G5)  &
            std_logic_vector(G6)  &
            std_logic_vector(G7)  &
            std_logic_vector(G8)  &
            std_logic_vector(G9)  &
            std_logic_vector(G10) &
            std_logic_vector(G11) &
            std_logic_vector(G12) &
            std_logic_vector(G13) &
            std_logic_vector(G14) &
            std_logic_vector(G15);
end Behavioral;
