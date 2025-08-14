----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/07/2025 03:22:59 PM
-- Design Name: 
-- Module Name: arbiter - Behavioral
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
library UNISIM;
use UNISIM.VComponents.all;

entity arbiter is
    generic (
        -- This is only used in the tapcarry arch
        TAP_IDX: integer := 16
    );
    port (
        data: in  std_logic_vector(1 downto 0);
        resp: out std_logic
    );
end arbiter;

architecture nodelay of arbiter is
    attribute DONT_TOUCH: boolean;
    attribute DONT_TOUCH of dff: label is true;
begin
    dff: FDRE port map (
        Q => resp,
        C => data(0),
        CE => '1',
        D => data(1),
        R => '0'
    );
end nodelay;

architecture lutdelay of arbiter is
    attribute DONT_TOUCH: boolean;
    attribute DONT_TOUCH of delay, dff: label is true;
    
    signal proxy: std_logic;
begin
    
    delay: LUT1 generic map (INIT => "10")
    port map (
        I0 => data(1),
        O  => proxy
    );

    dff: FDRE port map (
        Q => resp,
        C => data(0),
        CE => '1',
        D => proxy,
        R => '0'
    );
end lutdelay;

architecture carrytap of arbiter is
    attribute DONT_TOUCH: boolean;
    attribute DONT_TOUCH of delay, dff: label is true;
    
    signal din:   std_logic_vector(3 downto 0);
    signal proxy: std_logic_vector(3 downto 0);
begin
    
    din <= "000" & data(1);
    
    delay: CARRY4 
    port map (
        CI => '0', CYINIT => '0',
        DI => din,
        S  => "1110",
        CO => proxy,
        O  => open
    );

    dff: FDRE port map (
        Q => resp,
        C => data(0),
        CE => '1',
        D => proxy(TAP_IDX),
        R => '0'
    );
end carrytap;