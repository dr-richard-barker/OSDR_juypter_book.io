#!/usr/bin/env

# only requirement is jq, not using genelab-utils
conda activate genelab-utils

echo -e "OSD-id\thits\tpublicReleaseDate\tpublicReleaseDateYear\ttechnologyPlatform\ttechnologyType\tmeasurementType\tOrganismCount\tOrganism\tFactors" >> genelab_osd.txt

for i in {1..2000}; do

    echo "OSD-$i"
    url="https://osdr.nasa.gov//genelab/data/glds/meta/$i"
    response=$(curl -s $url)

    hits=$(echo $response  | jq '.hits')

    if [  "$hits" != "0" ]; then
        echo "$hits hit(s) found for OSD-$i "

        ID=$(echo $response | jq '.study' | jq -r 'keys_unsorted' | jq -r '.[0]')
        # report first, few times I found:  1-Jan-16 and 01-Jan-2016
        publicReleaseDate=$(echo $response  | jq '.study' | jq '.. | select(.publicReleaseDate? and .publicReleaseDate != "") | .publicReleaseDate'  -r | head -n1 ) 
        # this can have more than 1 output
        technologyPlatform=$(echo $response  | jq '.study' | jq '.. | select(.technologyPlatform? and .technologyPlatform != "") | .technologyPlatform' )
        # this can have more than 1 output
        technologyType=$(echo $response  | jq '.study' | jq '.. | select(.technologyType?) | .technologyType' | jq '.annotationValue'   )
        # this can have more than 1 output
        measurementType=$(echo $response  | jq '.study' | jq '.. | select(.measurementType?) | .measurementType' | jq '.annotationValue'  )
        # this can have more than 1 output
        factor=$(echo $response  | jq '.study' | jq '.. | select(.factors?) | .factors' | jq -r '.[] | select(.factorName != null) | .factorName'  )

        species=$(echo $response  | jq '.study' | jq '.. | select(.organisms?) | .organisms' | jq '.links' -r | jq '.[]'  | sed -e 's/<[^>]*>//g' )

        # collapse species if more than 1
        arr0=()
        while read -r element; do
            # Remove leading and trailing spaces and quotes
            element_trimmed=${element##+([[:space:]])}
            element_trimmed=${element_trimmed%%+([[:space:]])}
            # Remove quotes
            element_without_quotes=${element_trimmed//\"/}
            element_without_quotes="${element_without_quotes%" "}"

    
            arr0+=("$element_without_quotes")
        done <<< "$species"
        # Initialize an empty string to store the collapsed elements
        collapsed_species=""

        # Get the length of the array
        arr_length=${#arr0[@]}
        # Iterate through the array elements and conditionally add a semicolon
        for ((i = 0; i < arr_length; i++)); do
            # Append the current element to the collapsed string
            collapsed_species+="${arr0[i]}"
    
            # Add a semicolon if it's not the last element
            if ((i < arr_length - 1)); then
                collapsed_species+=";"
            fi
        done


        # collapse factor if more than 1
        arr4=()
        while read -r element; do
            # Remove leading and trailing spaces and quotes
            element_trimmed=${element##+([[:space:]])}
            element_trimmed=${element_trimmed%%+([[:space:]])}
            # Remove quotes
            element_without_quotes=${element_trimmed//\"/}
            element_without_quotes="${element_without_quotes%" "}"

            arr4+=("$element_without_quotes")
        done <<< "$factor"
        # Initialize an empty string to store the collapsed elements
        collapsed_factors=""

        # Get the length of the array
        arr_length4=${#arr4[@]}
        # Iterate through the array elements and conditionally add a semicolon
        for ((i = 0; i < arr_length4; i++)); do
            # Append the current element to the collapsed string
            collapsed_factors+="${arr4[i]}"
    
            # Add a semicolon if it's not the last element
            if ((i < arr_length4 - 1)); then
                collapsed_factors+=";"
            fi
        done

        
        publicReleaseDateYear=$(date -d $publicReleaseDate "+%Y")
        echo $ID
        echo $publicReleaseDateYear
        echo $technologyPlatform
        echo $technologyType
        echo $measurementType
        echo $collapsed_species
        echo $collapsed_factors

        # Initialize an empty array
        arr1=()
        arr2=()
        arr3=()
        # Use a while loop to read each element and add it to the array
        while read -r element; do
            # Remove quotes using parameter expansion
            element_without_quotes=${element//\"/}
            arr1+=("$element_without_quotes")
          #arr1+=("$element" )
        done <<< "$technologyPlatform" 

        while read -r element; do
            element_without_quotes=${element//\"/}
            arr2+=("$element_without_quotes")
        done <<< "$technologyType"

        while read -r element; do
            element_without_quotes=${element//\"/}
            arr3+=("$element_without_quotes")
        done <<< "$measurementType"

        length1=${#arr1[@]}
        length2=${#arr2[@]}
        length3=${#arr3[@]}

        for ((element = 0; element <= length1-1; element++)); do
            echo "Element: ${arr1[$element]} "
            echo "Element: ${arr2[$element]} "
            echo "Element: ${arr3[$element]} "
            echo -e "$ID\t$length1\t$publicReleaseDate\t$publicReleaseDateYear\t${arr1[$element]}\t${arr2[$element]}\t${arr3[$element]}\t$arr_length\t$collapsed_species\t$collapsed_factors" >> genelab_osd.txt
        done

    else
        echo "No match exist for OSD-$i "

    fi
done
