conda info --envs | grep -w "$ENV_NAME" > /dev/null
if [ $? -eq 0 ]; then
    echo "Activating Conda environment $ENV_NAME"
else
    echo "Creating and activating new Conda environment $ENV_NAME with Python 3.10"
    conda create -n "$ENV_NAME" python=3.10
fi

if [ -f requirements.txt ]; then
    conda run -n "$ENV_NAME" pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping additional package installations."
fi