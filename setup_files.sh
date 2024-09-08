#!/bin/bash

# Create environment directories
mkdir -p environments/{dev,staging,prod}

# Create module directories
mkdir -p modules/{networking,compute,database}

# Create scripts directory
mkdir scripts

# Create environment files
for env in dev staging prod; do
    touch environments/$env/{main.tf,variables.tf,outputs.tf}
done

# Create README file
touch README.md

# Create sample module files
for module in networking compute database; do
    touch modules/$module/{main.tf,variables.tf,outputs.tf}
done

# Print the structure
echo "Terraform project structure created:"
tree

echo "Project structure created successfully!"