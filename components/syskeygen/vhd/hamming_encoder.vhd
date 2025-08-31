library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ham_encoder is 
  port( 
  message  : in  std_logic_vector(48 downto 0);
  encoding : out std_logic_vector(76 downto 0);
  parities: out std_logic_vector(27 downto 0)
        );
end entity;
architecture behav of ham_encoder is 
begin 
    process(message)
        variable block_data : std_logic_vector(6 downto 0);
        variable block_enc  : std_logic_vector(10 downto 0);
        variable temp_enc   : std_logic_vector(76 downto 0);
        variable idx        : integer;
    begin
    temp_enc := (others => '0');  -- clear first
    for b in 0 to 6 loop
            idx := b*7;
            block_data := message(idx+6 downto idx);
            
            block_enc(2)  := block_data(0);
            block_enc(4)  := block_data(1);
            block_enc(5)  := block_data(2);
            block_enc(6)  := block_data(3);
            block_enc(8)  := block_data(4);
            block_enc(9)  := block_data(5);
            block_enc(10) := block_data(6);

            -- compute parity bits 
            block_enc(0) := block_enc(2) xor block_enc(4) xor block_enc(6) xor block_enc(8) xor block_enc(10);
            block_enc(1) := block_enc(2) xor block_enc(5) xor block_enc(6) xor block_enc(9) xor block_enc(10);
            block_enc(3) := block_enc(4) xor block_enc(5) xor block_enc(6);
            block_enc(7) := block_enc(8) xor block_enc(9) xor block_enc(10);
            
            parities(b * 4) <= block_enc(0);
            parities(b * 4 + 1) <= block_enc(1);
            parities(b * 4 + 2) <= block_enc(2);
            parities(b * 4 + 3) <= block_enc(3);
            
            -- copy into output variable
            temp_enc((b*11)+10 downto b*11) := block_enc;
        end loop;
        encoding <= temp_enc;
    end process;
end behav;


