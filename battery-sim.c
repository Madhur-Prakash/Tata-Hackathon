#include "contiki.h"
#include "sys/log.h"
#include "dev/battery-sensor.h"

#define LOG_MODULE "BatterySim"
#define LOG_LEVEL LOG_LEVEL_INFO

PROCESS(battery_sim_process, "Battery Simulation Process");
AUTOSTART_PROCESSES(&battery_sim_process);

static int battery = 100; // Start at 100%

PROCESS_THREAD(battery_sim_process, ev, data)
{
  static struct etimer timer;

  PROCESS_BEGIN();

  SENSORS_ACTIVATE(battery_sensor);

  etimer_set(&timer, CLOCK_SECOND * 5); // Every 5 seconds

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));

    if(battery > 0) {
      battery -= 5; // Simulate drain
    }

    LOG_INFO("Battery: %d%%\n", battery);

    etimer_reset(&timer);
  }

  PROCESS_END();
}

