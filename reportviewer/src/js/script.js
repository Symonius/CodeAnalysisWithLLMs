function createDebugInfoButton(rawData) {
    // If rawData doesn't exist, return an empty string.
    if (!rawData) {
        return '';
    }

    // Format the JSON content for the popover's data attribute.
    // We use <pre> and <code> for nice formatting inside the popover.
    const popoverContent = `
        <h6>Endpoint</h6>
        <pre><code>${JSON.stringify(rawData.endpoint, null, 2)}</code></pre>
        <h6>Headers</h6>
        <pre><code>${JSON.stringify(rawData.headers, null, 2)}</code></pre>
        <h6>Body</h6>
        <pre><code>${JSON.stringify(rawData.body, null, 2)}</code></pre>
    `.replace(/"/g, '&quot;'); // Escape quotes for the HTML attribute

    return `
    <img src="img/bootstrap/card-text.svg" 
         alt="Info" 
         width="24" 
         height="24"
         class="ms-2 info-popover-trigger"
         style="cursor: pointer;"
         data-bs-toggle="popover"
         data-bs-placement="left"
         data-bs-html="true"
         title="Raw API Request"
         data-bs-content="${popoverContent}"
		 data-bs-custom-class="popover-wide">`;
}


const fileInput = document.getElementById('fileInput');
const reportDataDisplay = document.getElementById('report_data');

// Event listener for when a file is selected via the input
fileInput.addEventListener('change', (event) => {
    const files = event.target.files; // Get the FileList object

    if (files.length > 0) {
        const selectedFile = files[0]; // Get the first (and only) selected file
        const reader = new FileReader();

        // This function will be called when the file is successfully read
        reader.onload = (e) => {
            try {
                const repData = JSON.parse(e.target.result);

                let report_string = "<h2>Report Summary</h2>";
                report_string += "<p>Date: " + repData.report_timestamp + "</p>";
				report_string += "<p>Folder Path: " + repData.scfolder + "</p>";
                report_string += "<p>Model: " + repData.analysis_details.model + "</p>";
				report_string += "<p>Type of Prompt: " + repData.prompttype + "</p>";
				report_string += "<p>Temperature: " + repData.analysis_details.config.temperature + "</p>";
                report_string += "<p>Files successfully analyzed: " + repData.vulnerabilities_found.filter(vul => vul.response_code_api_query == 200).length + "/" + repData.vulnerabilities_found.length + "</p>";
				report_string += "<p>Total detected vulnerabilities: <span id='totalvuls'></span></p>";
				report_string += `<div class="accordion-item">
                        <h2 class="accordion-header" id="heading-system">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-system" aria-expanded="false" aria-controls="collapse-system">
                                system_prompt
							</button>
                        </h2>
                        <div id="collapse-system" class="accordion-collapse collapse" aria-labelledby="heading-system" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
								${repData.analysis_details.sysprompt}
							</div>
                        </div>
                    </div>
				<div class="accordion-item">
                        <h2 class="accordion-header" id="heading-user">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-user" aria-expanded="false" aria-controls="collapse-user">
                                user_prompt
							</button>
                        </h2>
                        <div id="collapse-user" class="accordion-collapse collapse" aria-labelledby="heading-user" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
								${repData.analysis_details.userprompt}
							</div>
                        </div>
                    </div><br><br>`
				
                
				let accordion = 0;
                report_string += `<div class="accordion" id="accordionExample">`;
                let totalvuls = 0;
				repData.vulnerabilities_found.forEach(vul => {
                    accordion++;
					// Get the count of vulnerabilities
					const vulnerabilitiesCount = vul.vulnerabilities.length;
					totalvuls += vulnerabilitiesCount;

                    report_string += `
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="heading-${accordion}">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${accordion}" aria-expanded="false" aria-controls="collapse-${accordion}">
                                ${vul.response_code_api_query} | ${vul.filename} | Vulnerabilities:&nbsp<span style="${vulnerabilitiesCount > 0 ? 'color:red;' : ''}">${vulnerabilitiesCount}</span></button>																							
                        </h2>
                        <div id="collapse-${accordion}" class="accordion-collapse collapse" aria-labelledby="heading-${accordion}" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
							${createDebugInfoButton(vul.raw)}
	
							<div class="scaleable-wrapper">
								<div id="block">
									<pre><code class="sourcecode"></code></pre>
								</div>
							</div>
								
                                <div class="accordion" id="sub-accordionExample-${accordion}">`;

                    let subaccordion = 0;
                    vul.vulnerabilities.forEach(detvul => {
                        subaccordion++;
                        report_string += `<div class="accordion-item">
                            <h2 class="accordion-header" id="sub-heading-${accordion}-${subaccordion}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#sub-collapse-${accordion}-${subaccordion}" aria-expanded="false" aria-controls="sub-collapse-${accordion}-${subaccordion}">
                                    Line:&nbsp${detvul.code_line} | ${detvul.vulnerability_id}
                                </button>
                            </h2>
                            <div id="sub-collapse-${accordion}-${subaccordion}" class="accordion-collapse collapse" aria-labelledby="sub-heading-${accordion}-${subaccordion}" data-bs-parent="#sub-accordionExample-${accordion}">
                                <div class="accordion-body">
                                    <p>${detvul.description}</p>
                                </div>
                            </div>
                        </div>`;
                    });

                    report_string += `
                                </div>
                            </div>
                        </div>
                    </div>`;
                });
				
				
                reportDataDisplay.innerHTML = report_string;
				document.getElementById('totalvuls').innerHTML = totalvuls;
				let sourcecodefields = document.getElementsByClassName("sourcecode")
				repData.vulnerabilities_found.forEach((vul, idx) => {
					sourcecodefields[idx].textContent = vul.file_content;
				});
			
				makeblockwork();
				
				// Find all elements that are meant to be popover triggers
				const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');

				// Loop through each trigger element
				popoverTriggerList.forEach(popoverTriggerEl => {
					// Initialize the Bootstrap Popover on the element
					new bootstrap.Popover(popoverTriggerEl);					
				});
	
            } catch (error) {
                reportDataDisplay.innerHTML = "<p>Error parsing JSON file: " + error.message + "</p>";
                console.error('JSON parsing error:', error);
            }
        };

        // This function will be called if there's an error reading the file
        reader.onerror = (e) => {
            reportDataDisplay.textContent = `Error reading file: ${e.target.error.name}`;
            console.error('File reading error:', e.target.error);
        };

        // Start reading the file as text
        reader.readAsText(selectedFile);
    } else {
        reportDataDisplay.textContent = 'No file selected. Please choose a file.';
    }
});


