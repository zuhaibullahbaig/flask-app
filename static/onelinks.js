let linkCount = 0;
let noofcount = document.getElementById('noofcount');

document.getElementById('add_link').addEventListener('click', function() {
    try {
        const linkContainer = document.getElementById('new-links');
        const linkSet = document.createElement('div');
        
        if (linkCount == 0) {
            // You can assign a unique ID here
            linkSet.innerHTML = `
                <div id='link_4'>
                    <p class="link-description"> Link Four   </p>
                    <input type="text" name="link-four-name" placeholder="Link Name">
                    <input type="text" name="link-four-url" placeholder="Link URL">
                </div>
            `;
            linkCount++;

        } else if (linkCount == 1) {
            // You can assign a unique ID here
            linkSet.innerHTML = `
                <div id='link_5'>
                    <p class="link-description"> Link Five   </p>
                    <input type="text" name="link-five-name" placeholder="Link Name">
                    <input type="text" name="link-five-url" placeholder="Link URL">
                </div>
            `;
            linkCount++;

        } else if (linkCount == 2) {
            // You can assign a unique ID here
            linkSet.innerHTML = `
                <div id='link_6'>
                    <p class="link-description"> Link Six   </p>
                    <input type="text" name="link-six-name" placeholder="Link Name">
                    <input type="text" name="link-six-url" placeholder="Link URL">
                </div>
            `;
            linkCount++;
        } else if (linkCount == 3) {
            linkSet.innerHTML = `
                <div id='link_7'> 
                    <p class="link-description"> No more links can be added    </p>
                </div>
            `;
            linkCount++;

        } else {
            return;
        }
        linkContainer.appendChild(linkSet);
    } catch (error) {
        return ;
    }
    noofcount.value = linkCount;

});

document.getElementById('remove_link').addEventListener('click', function() {
    try {
        if (linkCount == 4) {
            deleting_element = document.getElementById('link_6');
            deleting_element.parentNode.removeChild(deleting_element);
            enough = document.getElementById('link_7');
            enough.parentNode.removeChild(enough);
            linkCount = 2;
        } else if (linkCount == 3 ) {
            deleting_element = document.getElementById('link_6');
            deleting_element.parentNode.removeChild(deleting_element);
            linkCount--;
        } else if (linkCount == 2) {
            deleting_element = document.getElementById('link_5');
            deleting_element.parentNode.removeChild(deleting_element);
            linkCount--;
        } else if (linkCount == 1) {
            deleting_element = document.getElementById('link_4');
            deleting_element.parentNode.removeChild(deleting_element);
            linkCount--;

        } else {
            linkCount = 0;
        }
    } catch (error) {
        return;
    }
    noofcount.value = linkCount;

});


  // Function to update the custom tag with the selected file name
  function updateFileName(input) {
        const fileNameTag = document.getElementById("file-name");
        if (input.files.length > 0) {
            fileNameTag.textContent = input.files[0].name;
        } else {
            fileNameTag.textContent = "";
        }
    }






    const templateElements = document.querySelectorAll('[id^="template_"]');
    const iconElements = document.querySelectorAll('[id^="icon"]');
    const selectElement = document.getElementById("templateSelector");

    // Add click event listeners to template elements
    templateElements.forEach((template, index) => {
        template.addEventListener('click', () => {
            // Remove "active" class from all icons
            iconElements.forEach((icon) => {
                icon.classList.remove("active");
            });
            // Add "active" class to the corresponding icon
            iconElements[index].classList.add("active");
            // Set the select value to match the clicked template
            selectElement.value = template.id;
        });
    });




    