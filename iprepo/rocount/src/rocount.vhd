library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
 
entity rocount is
    Port (
        reset : in std_logic ;
        clk   : in std_logic ;
        cen   : in std_logic;                       -- Counter enable (Note: We said we'd change it to a single one)
        sel   : in  std_logic_vector(2 downto 0);  -- 16x3-bit selects flattened
        count : out std_logic_vector(383 downto 0); -- 16x24-bit ou tputs flattened
        busy  : out std_logic
    );
end rocount;
 
architecture Structural of rocount is
  attribute MARK_DEBUG: boolean;
  attribute MARK_DEBUG of busy, cen, sel: signal is true;
  
  component TOP
    Port (
    clk   : in std_logic;
    reset : in std_logic ;       -- Asynchronous reset for the counter
    en   : in  std_logic;                      -- Enable all ROs
    sel  : in  std_logic_vector(2 downto 0);   -- Select RO output
    count : out std_logic_vector(23 downto 0)
    );
  end component;
  
  component Enable_counter 
        Generic (
            TARGET_VALUE: integer := 5_000_000;
            COUNTER_WIDTH: integer := 24
        );
        Port (
        clk:        in std_logic;
        reset:      in std_logic;
        enable:     in std_logic;
        RO_enable:  out std_logic_vector(15 downto 0);
        RO_reset:   out std_logic_vector(15 downto 0);
        busy:       out std_logic_vector(15 downto 0)
        );
   end component;
   
   signal RO_enable_int: std_logic_vector(15 downto 0);
   signal RO_reset_int:  std_logic_vector(15 downto 0);
   signal are_busy:      std_logic_vector(15 downto 0);
   signal rst_proxy:     std_logic;
   attribute MARK_DEBUG of are_busy: signal is true;
   
begin
     
  
  gen_instances : for i in 0 to 15 generate
    TOP_inst : TOP
      port map (
        clk   => clk,
        reset => RO_reset_int(i),
        en    => RO_enable_int(i),
--        sel   => sel((i*3 + 2) downto i*3),
        sel => sel,
        count => count((i*24 + 23) downto i*24)
      );
  end generate;
  
  Enable_inst : Enable_counter
  generic map (
    TARGET_VALUE => 500_000,
    COUNTER_WIDTH => 19
  )
  port map (
    clk => clk,
    reset     => reset,
    enable    => cen,
    RO_enable => RO_enable_int,
    RO_reset  => RO_reset_int,
    busy      => are_busy
  );
  
  -- Evaluate the busy flag (wont use or reduce)
  BUSY_EVAL: process (are_busy) 
    variable temp: std_logic := '0';
  begin
    temp := '0';
    
    for i in 0 to 4 loop
        temp := temp or are_busy(i);
    end loop;
    
    busy <= temp;
  end process;
 
 
 
end Structural;