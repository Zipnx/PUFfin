----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/15/2025 01:50:14 PM
-- Design Name: 
-- Module Name: controller - Behavioral
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

entity controller is
    generic (
        apuf_execs: integer := 3
    );
    port (
        clk, rst:   in  std_logic;
        trigger:    in  std_logic;
        apuf_trig:  out std_logic;
        apuf_busy:  in  std_logic;
        ec_rst:     out std_logic;
        ec_readen:  out std_logic;
        ec_trig:    out std_logic;
        ro_trig:    in  std_logic;
        ro_req:     out std_logic;
        ro_res:     in  std_logic;
        ro_loaded:  out std_logic;
        busy:       out std_logic
    );
end controller;

architecture Behavioral of controller is
    attribute MARK_DEBUG: boolean;
    
    -- Check the excalidraw drawing to understand this,
    -- warning this is from 2 hours of sleep, might change
    type state_t is (
        IDLE, 
        APUF_EXEC, EC_READ, APUF_AWAIT,
        RO_XCHG, RO_AWAIT,
        DONE
    );
    
    signal apuf_exec_counter: unsigned(3 downto 0) := (others => '0');
    signal ro_xchg_ongoing: std_logic := '0';
    
    signal curstate: state_t := IDLE;
    
    signal int_apuf_trig: std_logic := '0';
    signal int_ec_rst:    std_logic := '0';
    signal int_ec_readen: std_logic := '0';
    signal int_ec_trig:   std_logic := '0';
    signal int_ro_req:    std_logic := '0';
    signal int_ro_loaded: std_logic := '0';
    signal int_busy:      std_logic := '0';
    
    -- gotta catch em all
    attribute MARK_DEBUG of trigger, curstate, apuf_exec_counter, apuf_busy, 
                            int_apuf_trig, int_ec_readen, int_ec_trig, int_busy: signal is true;
    
    --attribute MARK_DEBUG of int_ro_req, ro_res, int_ro_loaded, ro_trig, ro_xchg_ongoing: signal is true;
begin
    apuf_trig   <= int_apuf_trig;
    ec_readen   <= int_ec_readen;
    ec_trig     <= int_ec_trig;
    ro_req      <= int_ro_req;
    ro_loaded   <= int_ro_loaded;
    busy        <= int_busy;
    
    CTRL_STATE: process (clk, rst) 
    begin
        
        if rst = '1' then
            
            int_busy <= '0';
            ec_rst <= '1';
            
            curstate <= IDLE;
            
        elsif rising_edge(clk) then
        
        -- Idk man, im tired
        -- TODO: Fix the reset, somehow being tied high, properly, this is just because
        --       its late and im tired fighting for my life in ILAs
        ec_rst <= '0';
        case curstate is
        
            --------------------------------------
            ----------- IDLE Switch --------------
            --------------------------------------
            when IDLE => 
                if trigger = '1' then
                    int_busy <= '1';
                    -- looks weird but is optimal i think
                    int_ec_trig <= '0';
                    curstate <= APUF_EXEC;
                elsif ro_trig = '1' then
                    int_busy <= '1';
                    int_ec_trig <= '0';
                    curstate <= RO_XCHG;
                end if;
            
            ------------------------------------
            ----- APUF OPERATION SEQUENCE ------
            ------------------------------------
            -- This is stupid, the "fsm" on rawapuf
            -- isnt even actually doing any control, its
            -- just to add 1CC of delay, when capturing the 
            -- response. Eitherway, for now this sucks, but works
            when APUF_EXEC => 
                curstate <= EC_READ;
            
            when EC_READ =>
                curstate <= APUF_AWAIT;
                
            when APUF_AWAIT => 
                if apuf_exec_counter = apuf_execs then
                    int_ec_trig <= '1';
                    int_busy <= '0';
                    curstate <= DONE;
                else
                    curstate <= APUF_EXEC;
                end if;
                
            -------------------------------------
            ------- RO EXCHANGE SEQUENCE --------
            -------------------------------------
            when RO_XCHG =>
                curstate <= RO_AWAIT;
            
            when RO_AWAIT =>
                if ro_res = '1' then
                    int_ro_loaded <= '1';
                    int_busy <= '0';
                    curstate <= DONE;
                else 
                    curstate <= curstate;
                end if;
            
            ------------------------------------
            --------- RESET FROM DONE ----------
            ------------------------------------
            when DONE =>
                if (trigger = '0' and ro_trig = '0') then
                    curstate <= IDLE;
                else
                    curstate <= curstate;
                end if;
            
            when others => 
                null;
        end case;
        end if;
        
    end process;
    
    CTRL_EXEC: process (clk) begin
        if rising_edge(clk) then
        case curstate is
            when IDLE => 
                int_ec_readen <= '0';
            ------------------------------------
            ----- APUF OPERATION SEQUENCE ------
            ------------------------------------
            when APUF_EXEC => 
                apuf_exec_counter <= apuf_exec_counter + 1;
                int_apuf_trig <= '1';
            when EC_READ => 
                int_ec_readen <= '1';
            when APUF_AWAIT => 
                int_apuf_trig <= '0';
                int_ec_readen <= '0';
                
            -------------------------------------
            ------- RO EXCHANGE SEQUENCE --------
            -------------------------------------
            when RO_XCHG => 
                int_ro_req <= '1';
            
            when RO_AWAIT => null;
            when DONE => 
                int_ro_req <= '0';
                apuf_exec_counter <= (others => '0');
            
        end case;
        end if;
    end process; 
    
end Behavioral;
