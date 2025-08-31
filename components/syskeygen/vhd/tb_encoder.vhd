----------------------------------------------------------------------------------
-- Testbench for 16-input Lehmer Encoder
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity encoder_tb is
end encoder_tb;

architecture Behavioral of encoder_tb is
    -- DUT signals
    signal C1, C2, C3, C4, C5, C6, C7, C8,
           C9, C10, C11, C12, C13, C14, C15, C16 : unsigned(23 downto 0);
    signal code_out : std_logic_vector(48 downto 0);

    component encoder
         Port (
            C1, C2, C3, C4, C5, C6, C7, C8,
            C9, C10, C11, C12, C13, C14, C15, C16 : in unsigned(23 downto 0);
            code_out : out std_logic_vector(48 downto 0)
         );
    end component ;
begin
    -- Instantiate DUT
    uut: encoder
        port map (
            C1 => C1,   C2 => C2,   C3 => C3,   C4 => C4,
            C5 => C5,   C6 => C6,   C7 => C7,   C8 => C8,
            C9 => C9,   C10 => C10, C11 => C11, C12 => C12,
            C13 => C13, C14 => C14, C15 => C15, C16 => C16,
            code_out => code_out
        );

    -- Test process
    stim_proc: process
    begin
        report "=== Starting Testbench for 16-input Encoder ===";

        -- Test 1: All equal
        for i in 1 to 16 loop
            case i is
                when 1  => C1  <= to_unsigned(5, 24);
                when 2  => C2  <= to_unsigned(5, 24);
                when 3  => C3  <= to_unsigned(5, 24);
                when 4  => C4  <= to_unsigned(5, 24);
                when 5  => C5  <= to_unsigned(5, 24);
                when 6  => C6  <= to_unsigned(5, 24);
                when 7  => C7  <= to_unsigned(5, 24);
                when 8  => C8  <= to_unsigned(5, 24);
                when 9  => C9  <= to_unsigned(5, 24);
                when 10 => C10 <= to_unsigned(5, 24);
                when 11 => C11 <= to_unsigned(5, 24);
                when 12 => C12 <= to_unsigned(5, 24);
                when 13 => C13 <= to_unsigned(5, 24);
                when 14 => C14 <= to_unsigned(5, 24);
                when 15 => C15 <= to_unsigned(5, 24);
                when 16 => C16 <= to_unsigned(5, 24);
                when others => null;
            end case;
        end loop;
        wait for 10 ns;
       -- report "Test 1 (All Equal) -> code_out = " & to_string(code_out);

        -- Test 2: Strictly increasing
        C1  <= to_unsigned(1, 24);  C2  <= to_unsigned(2, 24);
        C3  <= to_unsigned(3, 24);  C4  <= to_unsigned(4, 24);
        C5  <= to_unsigned(5, 24);  C6  <= to_unsigned(6, 24);
        C7  <= to_unsigned(7, 24);  C8  <= to_unsigned(8, 24);
        C9  <= to_unsigned(9, 24);  C10 <= to_unsigned(10, 24);
        C11 <= to_unsigned(11, 24); C12 <= to_unsigned(12, 24);
        C13 <= to_unsigned(13, 24); C14 <= to_unsigned(14, 24);
        C15 <= to_unsigned(15, 24); C16 <= to_unsigned(16, 24);
        wait for 10 ns;
       -- report "Test 2 (Increasing) -> code_out = " & to_string(code_out);

        -- Test 3: Strictly decreasing
        C1  <= to_unsigned(160, 24); C2  <= to_unsigned(150, 24);
        C3  <= to_unsigned(140, 24); C4  <= to_unsigned(130, 24);
        C5  <= to_unsigned(120, 24); C6  <= to_unsigned(110, 24);
        C7  <= to_unsigned(100, 24); C8  <= to_unsigned(90, 24);
        C9  <= to_unsigned(80, 24);  C10 <= to_unsigned(70, 24);
        C11 <= to_unsigned(60, 24);  C12 <= to_unsigned(50, 24);
        C13 <= to_unsigned(40, 24);  C14 <= to_unsigned(30, 24);
        C15 <= to_unsigned(20, 24);  C16 <= to_unsigned(10, 24);
        wait for 10 ns;
       -- report "Test 3 (Decreasing) -> code_out = " & to_string(code_out);

        -- Test 4: Random order
        C1  <= to_unsigned(100, 24); C2  <= to_unsigned(300, 24);
        C3  <= to_unsigned(200, 24); C4  <= to_unsigned(400, 24);
        C5  <= to_unsigned(150, 24); C6  <= to_unsigned(50, 24);
        C7  <= to_unsigned(175, 24); C8  <= to_unsigned(90, 24);
        C9  <= to_unsigned(225, 24); C10 <= to_unsigned(350, 24);
        C11 <= to_unsigned(10, 24);  C12 <= to_unsigned(60, 24);
        C13 <= to_unsigned(130, 24); C14 <= to_unsigned(70, 24);
        C15 <= to_unsigned(250, 24); C16 <= to_unsigned(15, 24);
        wait for 10 ns;
      --  report "Test 4 (Random #1) -> code_out = " & to_string(code_out);

        -- Test 5: Another random
        C1  <= to_unsigned(12, 24);  C2  <= to_unsigned(7, 24);
        C3  <= to_unsigned(25, 24);  C4  <= to_unsigned(3, 24);
        C5  <= to_unsigned(18, 24);  C6  <= to_unsigned(99, 24);
        C7  <= to_unsigned(55, 24);  C8  <= to_unsigned(41, 24);
        C9  <= to_unsigned(63, 24);  C10 <= to_unsigned(77, 24);
        C11 <= to_unsigned(5, 24);   C12 <= to_unsigned(1, 24);
        C13 <= to_unsigned(88, 24);  C14 <= to_unsigned(32, 24);
        C15 <= to_unsigned(101, 24); C16 <= to_unsigned(45, 24);
        wait for 10 ns;
       -- report "Test 5 (Random #2) -> code_out = " & to_string(code_out);

        report "=== Testbench Completed ===";
        wait;
    end process;

   

end Behavioral;
