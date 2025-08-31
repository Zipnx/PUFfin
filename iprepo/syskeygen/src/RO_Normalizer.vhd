library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity RO_Normalizer is
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
end RO_Normalizer;

architecture Behavioral of RO_Normalizer is
    type results_array_t is array (0 to 15) of std_logic_vector(23 downto 0);
    type avg_array_t is array (0 to 2) of std_logic_vector(23 downto 0);  -- 3 averages

    -- Example averages (replace with real ones)
    constant avg_rom : avg_array_t := (
        x"000001",  -- avg0
        x"000002",  -- avg1
        x"000003"   -- avg2
    );

begin
    process(sel, counts)
        variable count_word : unsigned(23 downto 0);
        variable avg_word   : unsigned(23 downto 0);
        variable norm_word  : unsigned(23 downto 0);
        variable results    : results_array_t;
    begin
        -- universal average selected once
        avg_word := unsigned(avg_rom(to_integer(unsigned(sel))));

        for i in 0 to 15 loop
            count_word := unsigned(counts((i*24+23) downto i*24));

            -- absolute difference
            if count_word >= avg_word then
                norm_word := count_word - avg_word;
            else
                norm_word := avg_word - count_word;
            end if;

            results(i) := std_logic_vector(norm_word);
        end loop;

        -- assign results
        result0  <= results(0);
        result1  <= results(1);
        result2  <= results(2);
        result3  <= results(3);
        result4  <= results(4);
        result5  <= results(5);
        result6  <= results(6);
        result7  <= results(7);
        result8  <= results(8);
        result9  <= results(9);
        result10 <= results(10);
        result11 <= results(11);
        result12 <= results(12);
        result13 <= results(13);
        result14 <= results(14);
        result15 <= results(15);
    end process;
end Behavioral;
