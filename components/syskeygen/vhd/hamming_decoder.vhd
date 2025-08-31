library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity hamming_decoder is
    port (
        encoding  : in  std_logic_vector(76 downto 0);
        message   : out std_logic_vector(48 downto 0);
        corrected : out std_logic
    );
end entity;
architecture behav of hamming_decoder is 
begin 
    process(encoding)
        variable block_enc   : std_logic_vector(10 downto 0);
        variable block_data  : std_logic_vector(6 downto 0);
        variable synd        : std_logic_vector(3 downto 0);
        variable temp_message: std_logic_vector(48 downto 0);
        variable any_corrected : std_logic := '0';
        variable bit_err     : integer;
        variable idx         : integer;
    begin
         temp_message := (others => '0'); -- init
         any_corrected := '0';
        for b in 0 to 6 loop
            idx := b*11;
            block_enc := encoding(idx+10 downto idx);
            synd(0) := block_enc(0) xor block_enc(2) xor block_enc(4) xor block_enc(6) xor block_enc(8) xor block_enc(10);
            synd(1) := block_enc(1) xor block_enc(2) xor block_enc(5) xor block_enc(6) xor block_enc(9) xor block_enc(10);
            synd(2) := block_enc(3) xor block_enc(4) xor block_enc(5) xor block_enc(6);
            synd(3) := block_enc(7) xor block_enc(8) xor block_enc(9) xor block_enc(10);

            bit_err := to_integer(unsigned(synd));
            if bit_err /= 0 then
                block_enc(bit_err-1) := not block_enc(bit_err-1);
                any_corrected := '1';
            end if;
            
            block_data(0) := block_enc(2);
            block_data(1) := block_enc(4);
            block_data(2) := block_enc(5);
            block_data(3) := block_enc(6);
            block_data(4) := block_enc(8);
            block_data(5) := block_enc(9);
            block_data(6) := block_enc(10);

            idx := b*7;
            temp_message(idx+6 downto idx) := block_data;
        end loop;

        message <= temp_message;
        corrected <= any_corrected;
    end process;

end behav;