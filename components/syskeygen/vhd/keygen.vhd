----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/29/2025 10:43:18 PM
-- Design Name: 
-- Module Name: keygen - Behavioral
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

entity keygen is
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
    port (
        clk:        in  std_logic;
        rst:        in  std_logic;
        sel:        in  std_logic_vector(2 downto 0);
        trigger:    in  std_logic;
        key:        out std_logic_vector(127 downto 0);
        busy:       out std_logic;
        
        -- Future APUF intercom, unimplemented for now
        apuf_req: in  std_logic;
        apuf_res: out std_logic := '0';
        apuf_obf: out std_logic_vector(31 downto 0) := (others => '0')
    );
end keygen;

architecture Behavioral of keygen is
    
    component rocount_0 
        port (
            reset, clk, cen: in std_logic;
            sel: in std_logic_vector(2 downto 0);
            count: out std_logic_vector(383 downto 0);
            busy: out std_logic
        );
    end component;
    
    signal counts_internal: std_logic_vector(383 downto 0);
    
begin
    
    -- NOTE: This works rn because the post proc is combinatorial.
    --       Will need to handle the busy differently in the future
    ROPUF: rocount_0 port map (
        reset => rst, clk => clk, cen => trigger,
        sel => sel, count => counts_internal,
        busy => busy
    );
    
    -- rn gon hook the     
    POSTPROC: entity work.Post_processing
    generic map (
        ECC_ENABLE => ECC_ENABLE,
        ECC_PARITY0 => ECC_PARITY0,
        ECC_PARITY1 => ECC_PARITY1,
        ECC_PARITY2 => ECC_PARITY2,
        NORM_AVG0 => NORM_AVG0,
        NORM_AVG1 => NORM_AVG1,
        NORM_AVG2 => NORM_AVG2,
        HASH_ENABLE => HASH_ENABLE
    )
    port map (
        sel => sel, counts => counts_internal,
        code_out => key(48 downto 0) 
    );
    
end Behavioral;
