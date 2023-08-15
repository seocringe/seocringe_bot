import shutil
from aiogram import types
from datetime import datetime

async def run_script_command(message: types.Message, arg1, arg2, arg3):
    # Define the script
    script = """
    #!/bin/bash
    if [ $# -lt 3 ]; then 
        echo "Domain name or keywords are not specified"
        exit 1
    fi
    D=$1
    F=${2:-txt}
    K=$(echo $3 | tr ',' '|')
    DATE=$(date +%d%m%Y)
    FN="$DATE-$D-sitemap-urls.$F"
    MFN="$DATE-$D-metadata.$F"
    URLS=(/sitemap.xml /ru/sitemap.xml /ua/sitemap.xml /uk/sitemap.xml /en/sitemap.xml sitemap_ua.xml sitemap_uk.xml sitemap_ru.xml sitemap_en.xml)
    for U in ${URLS[@]}; do
        curl -s https://$D$U | grep -oP "<loc>\K[^<]*" | xargs -I {} curl -s {} | grep -oP "<loc>\K[^<]*" >> $FN
    done
    echo "File $FN has been successfully created"
    for U in ${URLS[@]}; do
        curl -s https://$D$U | grep -oP "<loc>\K[^<]*" | xargs -I {} curl -s {} | grep -oP "<title>\K[^<]*|<description>\K[^<]*|<h[1-6]>\K[^<]*" | grep -i -E $K >> $MFN
    done
    echo "File $MFN has been successfully created"
    cat $MFN
    """

    # Write the script to a file
    with open('fnxsitemap.sh', 'w') as f:
        f.write(script)

    # Make the script executable
    shutil.chmod('fnxsitemap.sh', 0o755)

    # Run the script with subprocess
    result = subprocess.run(['./fnxsitemap.sh', arg1, arg2, arg3], stdout=subprocess.PIPE, text=True)

    # Send the result as a text file
    filename = f"result_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(result.stdout)
    await bot.send_document(message.chat.id, types.InputFile(filename))

    # Cleanup
    os.remove('fnxsitemap.sh')
    os.remove(filename)
