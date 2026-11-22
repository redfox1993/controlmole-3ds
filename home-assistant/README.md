# Home Assistant bridge (phase 1)

This is an **initial, receiver-only prototype**, not a working 3DS sender or remote-control feature.

## Installation
1. In Home Assistant, enable packages under `homeassistant:` with `packages: !include_dir_named packages` if not already enabled.
2. Copy `controlmole.yaml` to `/config/packages/controlmole.yaml`.
3. Replace `REPLACE_WITH_LONG_RANDOM_PRIVATE_WEBHOOK_ID` with a secret generated locally (e.g. `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`).
4. Check configuration and restart Home Assistant.
5. Test from the LAN:
   `python3 test_webhook.py --ha http://homeassistant.local:8123 --webhook-id YOUR_SECRET --minutes 15`
6. Inspect `input_number.controlmole_3ds_used` and `sensor.medienzeit_verbleibend`.

**Important:** `sensor.vincent_android_used_minutes` is a placeholder for a future Family Link integration. Without it the template treats Android usage as 0. Do not use the resulting remaining-time sensor to enforce a real limit until Android reporting is connected and validated.

## Wire protocol proposal
Send a JSON POST to `/api/webhook/<secret>` on the local HA instance:
```json
{"device_id":"vincent-3ds","used_minutes":15}
```
`used_minutes` is the **total counted playtime since local midnight**, not an incremental delta. This prevents duplicate reports from double-counting. The endpoint is LAN-only and the webhook ID is a bearer secret. Do not publish it or expose the endpoint publicly.

## Next steps / limitations
- Implement and test the actual network sender on a physical 3DS. The Luma game plugin must not block the game or break when Wi-Fi is unavailable.
- Add authenticated budget fetching and enforce limits locally while offline.
- Handle clock drift, date rollover, stale reports, and games not covered by the plugin.
- Validate the unofficial Family Link source before enabling shared-budget enforcement.
- This phase has not been compiled or tested on real 3DS hardware.

## Experimental 3DS sender (new, not hardware-tested)

The game plugin now contains an **opt-in** HTTP POST reporter. It is disabled unless you create `sdmc:/3ds/ControlMole/ha.ini`:

```ini
url=http://192.168.1.10:8123/api/webhook/YOUR_PRIVATE_WEBHOOK_ID
```

Replace the address with your actual Home Assistant LAN IP and the webhook ID with the same private secret from the HA package. The plugin attempts to POST cumulative counted minutes roughly once a minute while a supported game is active. This does **not** implement receiving or enforcing a remote budget.

**Do not install this experimental plugin on a child's daily-use 3DS yet.** The network calls have not been compiled against the target toolchain or tested on real hardware; they may block or crash a game. The original local ControlMole plugin remains the safer choice until validation. A future revision should move network I/O to a bounded asynchronous worker, provide error logs, and avoid repeated service initialization.

The current Home Assistant receiver trusts the possession of the webhook URL and is not an authentication protocol for remote administration. Keep the webhook ID private and LAN-only.
