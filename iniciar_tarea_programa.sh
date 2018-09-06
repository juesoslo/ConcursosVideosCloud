#!/bin/bash

crontab -e
chmod u+x proceso_conversion/ejecutar_proceso_conversion.sh
*/5 * * * * proceso_conversion/ejecutar_proceso_conversion.sh