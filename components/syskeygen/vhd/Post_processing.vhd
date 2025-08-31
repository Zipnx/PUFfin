----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 24.08.2025 16:10:12
-- Design Name: 
-- Module Name: Post_processing - Behavioral
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity Post_processing is
  generic (
        ECC_ENABLE:     boolean := false;
        ECC_PARITY0:    std_logic_vector(27 downto 0) := (others => '0');
        ECC_PARITY1:    std_logic_vector(27 downto 0) := (others => '0');
        ECC_PARITY2:    std_logic_vector(27 downto 0) := (others => '0');
        NORM_AVG0:      unsigned(23 downto 0) := (others => '0');
        NORM_AVG1:      unsigned(23 downto 0) := (others => '0');
        NORM_AVG2:      unsigned(23 downto 0) := (others => '0');
        HASH_ENABLE:    boolean := false
    );
  Port (
    sel     : in  std_logic_vector(2 downto 0);    -- universal 3-bit selector
    counts  : in  std_logic_vector(383 downto 0);  -- 16 x 24-bit words
    code_out : out STD_LOGIC_VECTOR (48 downto 0)
   );
end Post_processing;

architecture Behavioral of Post_processing is
 component RO_Normalizer
     Port (
        sel     : in  std_logic_vector(2 downto 0);    -- universal 3-bit selector
        counts  : in  std_logic_vector(383 downto 0);  -- 16 x 24-bit words
        result0 : out std_logic_vector(23 downto 0);
        result1 : out std_logic_vector(23 downto 0);
        result2 : out std_logic_vector(23 downto 0);
        result3 : out std_logic_vector(23 downto 0);
        result4 : out std_logic_vector(23 downto 0);
        result5 : out std_logic_vector(23 downto 0);
        result6 : out std_logic_vector(23 downto 0);
        result7 : out std_logic_vector(23 downto 0);
        result8 : out std_logic_vector(23 downto 0);
        result9 : out std_logic_vector(23 downto 0);
        result10: out std_logic_vector(23 downto 0);
        result11: out std_logic_vector(23 downto 0);
        result12: out std_logic_vector(23 downto 0);
        result13: out std_logic_vector(23 downto 0);
        result14: out std_logic_vector(23 downto 0);
        result15: out std_logic_vector(23 downto 0)
    );
 end  component;
 
 -- TODO: Lower the input width, would stop the LUTs count from being 5k
 component encoder
    Port (
    C1, C2, C3, C4, C5, C6, C7, C8,
    C9, C10, C11, C12, C13, C14, C15, C16 : in unsigned(23 downto 0);
    code_out : out std_logic_vector(48 downto 0)  -- 49 bits
  );
 end component;
 
 component ent_compressor
    Port ( code_in : in STD_LOGIC_VECTOR (48 downto 0);
           code_out : out STD_LOGIC_VECTOR (48 downto 0));
 end component;
 
 ------------------------
 --signals 
 ------------------------
signal result0_int  : std_logic_vector(23 downto 0);
signal result1_int  : std_logic_vector(23 downto 0);
signal result2_int  : std_logic_vector(23 downto 0);
signal result3_int  : std_logic_vector(23 downto 0);
signal result4_int  : std_logic_vector(23 downto 0);
signal result5_int  : std_logic_vector(23 downto 0);
signal result6_int  : std_logic_vector(23 downto 0);
signal result7_int  : std_logic_vector(23 downto 0);
signal result8_int  : std_logic_vector(23 downto 0);
signal result9_int  : std_logic_vector(23 downto 0);
signal result10_int : std_logic_vector(23 downto 0);
signal result11_int : std_logic_vector(23 downto 0);
signal result12_int : std_logic_vector(23 downto 0);
signal result13_int : std_logic_vector(23 downto 0);
signal result14_int : std_logic_vector(23 downto 0);
signal result15_int : std_logic_vector(23 downto 0);
signal code_int : std_logic_vector(48 downto 0);
begin


Norm_inst : RO_Normalizer
port map(
        sel   => sel,   
        counts => counts,
        result0  => result0_int,
        result1  => result1_int,
        result2  => result2_int,
        result3  => result3_int,
        result4  => result4_int,
        result5  => result5_int,
        result6  => result6_int,
        result7  => result7_int,
        result8  => result8_int,
        result9  => result9_int,
        result10 => result10_int,
        result11 => result11_int,
        result12 => result12_int,
        result13 => result13_int,
        result14 => result14_int,
        result15 => result15_int
);

Enc_inst : encoder
port map (
        C1  => unsigned(result0_int),
        C2  => unsigned(result1_int),
        C3  => unsigned(result2_int),
        C4  => unsigned(result3_int),
        C5  => unsigned(result4_int),
        C6  => unsigned(result5_int),
        C7  => unsigned(result6_int),
        C8  => unsigned(result7_int),
        C9  => unsigned(result8_int),
        C10 => unsigned(result9_int),
        C11 => unsigned(result10_int),
        C12 => unsigned(result11_int),
        C13 => unsigned(result12_int),
        C14 => unsigned(result13_int),
        C15 => unsigned(result14_int),
        C16 => unsigned(result15_int),
        code_out => code_int
);

Comp_inst : ent_compressor
port map (
code_in => code_int,
code_out => code_out
);
end Behavioral;
