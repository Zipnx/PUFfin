----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 14.07.2025 11:00:54
-- Design Name: 
-- Module Name: Enable_counter - Behavioral
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

entity Enable_counter is
    generic (
        TARGET_VALUE: integer := 5_000_000;
        COUNTER_WIDTH: integer := 24
    );
    Port (
        clk:        in std_logic;
        reset:      in std_logic;
        -- Note: For the "enable" signal
        --       After i add the hacked together busy flag and the fsm, this works as a pulse trigger
        --       I am not changing its name, so i dont break your flows 
        enable:     in std_logic;
        RO_enable:  out std_logic_vector(15 downto 0);
        RO_reset:   out std_logic_vector(15 downto 0);
        busy:       out std_logic_vector(15 downto 0)
        
    );
end Enable_counter;

architecture Behavioral of Enable_counter is
    attribute MARK_DEBUG: boolean;
    constant TARGET : unsigned ( COUNTER_WIDTH - 1 downto 0) := to_unsigned(TARGET_VALUE, COUNTER_WIDTH); -- 0.1 second window for 50 Mhz clock 
    type state_t is (IDLE, ACTIVE, DONE);
    signal cur_state: state_t := IDLE;
    
    signal counter : unsigned ( COUNTER_WIDTH - 1 downto 0) := (others => '0');
    
    signal enable_reg: std_logic_vector(15 downto 0) := (others => '0');
    signal rorst_reg: std_logic_vector(15 downto 0) := (others => '0');
    
    attribute MARK_DEBUG of cur_state: signal is true;
begin
    
    RO_enable <= enable_reg;
    RO_reset  <= rorst_reg;
    busy      <= enable_reg;
    
    
    -- wiped the previous one, cooked together an fsm
    FSM: process (clk, reset)
    begin
        
        if reset = '1' then
            
            cur_state <= IDLE;
            enable_reg <= (others => '0');
        
        elsif rising_edge(clk) then
            
            if cur_state = IDLE then
                
                if enable = '1' then
                    rorst_reg <= (others => '1');
                    enable_reg <= (others => '1');
                    cur_state <= ACTIVE;
                    counter <= (others => '0');
                end if;
                
            elsif cur_state = ACTIVE then
                rorst_reg <= (others => '0');
                
                if counter = TARGET then
                    enable_reg <= (others => '0');
                    cur_state <= DONE;
                else
                    counter <= counter + 1;
                end if;
                
            elsif cur_state = DONE then
                
                if enable = '0' then
                    cur_state <= IDLE;
                end if;
                
            end if;
            
        end if;
        
    end process;
    
end Behavioral;
