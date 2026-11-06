(* ================================================================== *)
(* GENERÁLT — MetaSpace Studio (IEC 61131-3 ST back-end)   *)
(* Forrás cella: PacemakerSafetyCore — fail-closed safety guard    *)
(* ================================================================== *)
FUNCTION_BLOCK FB_PacemakerSafetyCore_Guard
VAR_INPUT
    battery : LREAL;
    sensor_stable : BOOL;
    heart_rate_cmd : LREAL;  (* javasolt *)
    rate_accel_cmd : LREAL;  (* javasolt *)
    rate_decel_cmd : LREAL;  (* javasolt *)
    interval_ms_cmd : LREAL;  (* javasolt *)
    Reset : BOOL;  (* latch nyugtázás *)
END_VAR
VAR_OUTPUT
    heart_rate : LREAL;  (* kiadott, biztonságos *)
    rate_accel : LREAL;  (* kiadott, biztonságos *)
    rate_decel : LREAL;  (* kiadott, biztonságos *)
    interval_ms : LREAL;  (* kiadott, biztonságos *)
    Fault : BOOL;
    Latched : BOOL;
END_VAR
VAR
    inv_upper_rate : BOOL;
    inv_lower_rate : BOOL;
    inv_smoothing : BOOL;
    inv_decel_limit : BOOL;
    inv_min_interval : BOOL;
    all_ok : BOOL;
END_VAR

IF Reset THEN
    Latched := FALSE;
END_IF;

IF Latched THEN
    heart_rate := 60.0;
    rate_accel := 0.0;
    rate_decel := 0.0;
    interval_ms := 250.0;
    Fault := TRUE;
ELSE
    inv_upper_rate := (heart_rate_cmd <= 165.0);
    inv_lower_rate := (heart_rate_cmd >= 40.0);
    inv_smoothing := (rate_accel_cmd <= 2.0);
    inv_decel_limit := (rate_decel_cmd <= 2.0);
    inv_min_interval := (interval_ms_cmd >= 250.0);
    all_ok := inv_upper_rate AND inv_lower_rate AND inv_smoothing AND inv_decel_limit AND inv_min_interval;
    IF all_ok THEN
        heart_rate := heart_rate_cmd;
        rate_accel := rate_accel_cmd;
        rate_decel := rate_decel_cmd;
        interval_ms := interval_ms_cmd;
        Fault := FALSE;
    ELSE
        heart_rate := 60.0;
        rate_accel := 0.0;
        rate_decel := 0.0;
        interval_ms := 250.0;
        Latched := TRUE;
        Fault := TRUE;
    END_IF;
END_IF;
END_FUNCTION_BLOCK