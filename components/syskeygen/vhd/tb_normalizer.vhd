library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_ro_normalizer is
end tb_ro_normalizer;

architecture sim of tb_ro_normalizer is

    component RO_Normalizer
       Port (
        sel     : in  std_logic_vector(31 downto 0);   -- 16 x 2-bit selectors
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
    end component;

    signal sel_tb    : std_logic_vector(31 downto 0);
    signal counts_tb : std_logic_vector(383 downto 0);

    signal result0_tb  : std_logic_vector(23 downto 0);
    signal result1_tb  : std_logic_vector(23 downto 0);
    signal result2_tb  : std_logic_vector(23 downto 0);
    signal result3_tb  : std_logic_vector(23 downto 0);
    signal result4_tb  : std_logic_vector(23 downto 0);
    signal result5_tb  : std_logic_vector(23 downto 0);
    signal result6_tb  : std_logic_vector(23 downto 0);
    signal result7_tb  : std_logic_vector(23 downto 0);
    signal result8_tb  : std_logic_vector(23 downto 0);
    signal result9_tb  : std_logic_vector(23 downto 0);
    signal result10_tb : std_logic_vector(23 downto 0);
    signal result11_tb : std_logic_vector(23 downto 0);
    signal result12_tb : std_logic_vector(23 downto 0);
    signal result13_tb : std_logic_vector(23 downto 0);
    signal result14_tb : std_logic_vector(23 downto 0);
    signal result15_tb : std_logic_vector(23 downto 0);

begin

    uut: RO_Normalizer
        port map (
            sel     => sel_tb,
            counts  => counts_tb,
            result0 => result0_tb,
            result1 => result1_tb,
            result2 => result2_tb,
            result3 => result3_tb,
            result4 => result4_tb,
            result5 => result5_tb,
            result6 => result6_tb,
            result7 => result7_tb,
            result8 => result8_tb,
            result9 => result9_tb,
            result10=> result10_tb,
            result11=> result11_tb,
            result12=> result12_tb,
            result13=> result13_tb,
            result14=> result14_tb,
            result15=> result15_tb
        );

    stim_proc: process
    begin
        -- Test case 1: sel=00, counts=0
        sel_tb    <= "00000000000000000000000000000000";
        counts_tb <= 
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000" &
            "000000000000000000000000";
        wait for 10 ns;

        -- Test case 2: sel=01, counts=1
        sel_tb    <= "01010101010101010101010101010101";
        counts_tb <= 
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001" &
            "000000000000000000000001";
        wait for 10 ns;

        -- Test case 3: sel=10, counts=2
        sel_tb    <= "10101010101010101010101010101010";
        counts_tb <= 
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010" &
            "000000000000000000000010";
        wait for 10 ns;

        wait;
    end process;

end sim;
