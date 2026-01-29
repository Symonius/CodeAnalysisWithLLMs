function makeblockwork() {
	// Select all 'pre code' elements
    $("pre code").each(function() {
        // Get the raw text content of the code block
        console.log($(this));
		const rawText = $(this).text();
		
		console.log(rawText);
        // Split the text into individual lines
        const lines = rawText.trim().split('\n');
        
        // Clear the original content of the code block
        $(this).empty();
        
        // Create a new span for each line and append it
        lines.forEach(lineText => {
            // Create a new <span> element for the line
            const $lineSpan = $("<span></span><br>").addClass("line");
            
            // Set the text content of the span. 
            // .text() automatically handles escaping, preventing HTML/XML interpretation.
            $lineSpan.text(lineText);
            
            // Append the new span to the code block
            $(this).append($lineSpan);
        });
    });

	var $el = $("#block");
	var elHeight = $el.outerHeight();
	var elWidth = $el.outerWidth();

	var $wrapper = $(".scaleable-wrapper");

	$wrapper.resizable({
		resize: doResize
	});

	function doResize(event, ui) {
		var scale;
		scale = Math.min(
			ui.size.width / elWidth,
			ui.size.height / elHeight
		);

		$el.css({
			transform: "translate(-50%, -50%) " + "scale(" + scale + ")"
		});
	}

	var starterData = {
		size: {
			width: $wrapper.width(),
			height: $wrapper.height()
		}
	}
	doResize(null, starterData);
}