----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/08/2025 02:24:56 PM
-- Design Name: 
-- Module Name: nxn_apuf - Behavioral
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

entity nxn_apuf is
    generic (
        BIT_WIDTH:     integer := 4;
        CHALL_BITS:    integer := 4;
        INTCONFIG:     std_logic_vector := "10"
    );
    port (
        clk:        in  std_logic;
        ipulse:     in  std_logic;
        challenge:  in  std_logic_vector(CHALL_BITS - 1 downto 0);
        response:   out std_logic_vector(BIT_WIDTH - 1 downto 0)
    );
end nxn_apuf;

architecture Behavioral of nxn_apuf is
    attribute MARK_DEBUG: boolean;
    
    constant CONFLEN: integer := BIT_WIDTH * 2;
    constant CONFIG: std_logic_vector(CONFLEN - 1 downto 0) := std_logic_vector(resize(unsigned(INTCONFIG), CONFLEN));
    
--    component clk_wiz_0
--        port (
--            clk_in1: in std_logic;
--            reset: in std_logic;
--            ila_clk: out std_logic;
--            locked: out std_logic
--        );
--    end component;
    
    signal clk_ila: std_logic;
    
    -- Using it for ILA on the response
    signal response_internal: std_logic_vector(BIT_WIDTH - 1 downto 0);
    attribute MARK_DEBUG of response_internal: signal is true;
    attribute MARK_DEBUG of challenge: signal is true;
    attribute MARK_DEBUG of ipulse: signal is true;
begin
    
--    CLK_WIZ_INST: clk_wiz_0 port map (
--        clk_in1 => clk,
--        reset => '0',
--        ila_clk => clk_ila,
--        locked => open
--    );
    
    N_APUF_GEN: for i in 0 to BIT_WIDTH - 1 generate
        
        N_APUF_INST: entity work.apuf
        generic map (
            CHALL_BITS => CHALL_BITS,
            CONFIG => CONFIG((i+1)*2 - 1 downto i*2)
        )
        port map (
            CLK => clk,
            IPULSE => ipulse,
            CHALLENGE => challenge,
            RESPONSE  => response_internal(i)
        ); 
        
    end generate;
    
    response <= response_internal;
    
end Behavioral;
