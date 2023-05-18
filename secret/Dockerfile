# Use an official Vault runtime as the base image
FROM vault:latest

# Set the working directory in the container
WORKDIR /vault

# Copy the app code to the container
COPY init.sh .

COPY vault.hcl /vault/config

# Expose the port that the app will run on
EXPOSE 8200

# Run the app when the container starts
CMD ["/bin/sh", "/vault/init.sh"]
