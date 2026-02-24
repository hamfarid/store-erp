#!/bin/bash

# Update download_global.sh
sed -i 's/v40\.3/Global System Ultimate/g' ./download_global.sh

# Update scripts/init_new_project.sh
sed -i 's/v40\.3/Global System Ultimate/g' ./scripts/init_new_project.sh

# Update scripts/upgrade_to_v37.sh
sed -i 's/v40\.3/Global System Ultimate/g' ./scripts/upgrade_to_v37.sh

# Update scripts/upgrade_to_v38.sh
sed -i 's/v40\.3/Global System Ultimate/g' ./scripts/upgrade_to_v38.sh

# Update infrastructure/Dockerfile.template
sed -i 's/v40\.4/Global System Ultimate/g' ./infrastructure/Dockerfile.template

# Update infrastructure/terraform/main.tf
sed -i 's/v40\.6/Global System Ultimate/g' ./infrastructure/terraform/main.tf

# Update scripts/upload_global_to_github.sh
sed -i 's/v40\.3/Global System Ultimate/g' ./scripts/upload_global_to_github.sh

# Update scripts/download_global_from_github.sh
sed -i 's/v40\.3/Global System Ultimate/g' ./scripts/download_global_from_github.sh

echo "Manual updates complete."
