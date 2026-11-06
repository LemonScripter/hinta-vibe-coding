# ==========================================================================
# GENERÁLT — MetaSpace Studio (Python back-end)
# Forrás cella: PacemakerSafetyCore   |   fail-closed enforcement
# NE szerkeszd kézzel — a .bio specifikációból regenerálódik.
# ==========================================================================
import metaspace_guard as _mg
from metaspace_guard import (SafetyKernel, SafetySpec,
                             Invariant, Guard)

def _inv_upper_rate(env, _k):
    return (env['heart_rate'] <= 165.0)

def _inv_lower_rate(env, _k):
    return (env['heart_rate'] >= 40.0)

def _inv_smoothing(env, _k):
    return (env['rate_accel'] <= 2.0)

def _inv_decel_limit(env, _k):
    return (env['rate_decel'] <= 2.0)

def _inv_min_interval(env, _k):
    return (env['interval_ms'] >= 250)

SPEC = SafetySpec(
    cell='PacemakerSafetyCore',
    signals={'heart_rate': (0.0, 300.0), 'rate_accel': (0.0, 50.0), 'rate_decel': (0.0, 50.0), 'interval_ms': (0.0, 5000.0), 'battery': (0.0, 100.0), 'sensor_stable': None},
    invariants=[Invariant('upper_rate', _inv_upper_rate), Invariant('lower_rate', _inv_lower_rate), Invariant('smoothing', _inv_smoothing), Invariant('decel_limit', _inv_decel_limit), Invariant('min_interval', _inv_min_interval)],
    safe_state={'heart_rate': 60.0, 'interval_ms': 250.0},
    default_on_violation='safe_state',
)

kernel = SafetyKernel(SPEC)
guard = Guard(kernel)

# Használat:
#   @guard.actuator('<jel>', on_violation='block'|'clamp'|'safe_state')
#   def set_x(value): ...        # value a védett aktuátor-írás
#   @guard.sensor('<jel>')
#   def read_y(): ...            # a visszaadott érték a szenzor
#
# INDÍTÁSI SZERZŐDÉS (kötelező) — különben az őr az első hívásnál latch-el:
#   A kernel minden jelet látni akar, mielőtt dönt; a HIÁNYZÓ érték fail-closed
#   sértés. Ha a vezérlő pl. csak az egyik szenzort olvassa be először, a
#   @guard.sensor azonnal safe-state-be zár, és az őr nem fut, amíg fel nem oldod.
#   Szenzorok : battery, sensor_stable
#   Aktuátorok: heart_rate, rate_accel, rate_decel, interval_ms
#   1. Olvasd be EGYSZER az összes fenti szenzort (a @guard.sensor-os függvényeken át).
#   2. Hívd:  kernel.reset()   # a latch kézi feloldása (nyugtázás)
#   3. Csak ezután indítsd a vezérlőciklust.
#   A safe-state/latch utána is csak reset()-tel oldódik; azt, hogy az ok megszűnt-e,
#   a hívó felelőssége ellenőrizni — a reset() nem vizsgálja.
