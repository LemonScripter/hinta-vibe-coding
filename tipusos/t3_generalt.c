/* ============================================================ */
/* GENERÁLT — MetaSpace Studio (C back-end) — cella: PacemakerSafetyCore
   fail-closed safety guard; NE szerkeszd kézzel. */
/* ============================================================ */
#include <math.h>
#include <stdbool.h>

typedef struct {
    bool latched;
} PacemakerSafetyCore_State;

typedef struct {
    double heart_rate;   /* kiadott, biztonságos */
    double rate_accel;   /* kiadott, biztonságos */
    double rate_decel;   /* kiadott, biztonságos */
    double interval_ms;   /* kiadott, biztonságos */
    bool fault;
    bool latched;
} PacemakerSafetyCore_Out;

PacemakerSafetyCore_Out PacemakerSafetyCore_guard(double battery, double sensor_stable, double heart_rate_cmd, double rate_accel_cmd, double rate_decel_cmd, double interval_ms_cmd, bool reset, PacemakerSafetyCore_State* st) {
    PacemakerSafetyCore_Out o;
    if (reset) { st->latched = false; }
    if (st->latched) {
        o.heart_rate = 60.0;
        o.rate_accel = 0.0;
        o.rate_decel = 0.0;
        o.interval_ms = 250.0;
        o.fault = true; o.latched = true;
        return o;
    }
    bool inv_upper_rate = (heart_rate_cmd <= 165.0);
    bool inv_lower_rate = (heart_rate_cmd >= 40.0);
    bool inv_smoothing = (rate_accel_cmd <= 2.0);
    bool inv_decel_limit = (rate_decel_cmd <= 2.0);
    bool inv_min_interval = (interval_ms_cmd >= 250.0);
    bool all_ok = inv_upper_rate && inv_lower_rate && inv_smoothing && inv_decel_limit && inv_min_interval;
    if (all_ok) {
        o.heart_rate = heart_rate_cmd;
        o.rate_accel = rate_accel_cmd;
        o.rate_decel = rate_decel_cmd;
        o.interval_ms = interval_ms_cmd;
        o.fault = false;
    } else {
        o.heart_rate = 60.0;
        o.rate_accel = 0.0;
        o.rate_decel = 0.0;
        o.interval_ms = 250.0;
        st->latched = true; o.fault = true;
    }
    o.latched = st->latched;
    return o;
}