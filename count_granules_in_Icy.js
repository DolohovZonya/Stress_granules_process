importClass(Packages.icy.gui.dialog.MessageDialog);
importClass(Packages.icy.sequence.Sequence);
importClass(Packages.icy.file.Loader);
importClass(Packages.plugins.fab.spotDetector.detector.UDWTWavelet);
importClass(Packages.icy.roi.ROI2DRectangle);
importClass(Packages.org.apache.poi.xssf.usermodel.XSSFWorkbook);
importClass(Packages.org.apache.poi.ss.usermodel.Workbook);
importClass(Packages.org.apache.poi.ss.usermodel.Sheet);
importClass(Packages.org.apache.poi.ss.usermodel.Row);
importClass(Packages.org.apache.poi.ss.usermodel.Cell);
importClass(Packages.java.io.FileOutputStream);
importClass(java.awt.geom.Point2D);
importClass(Packages.plugins.tprovoost.scripteditor.uitools.filedialogs.FileDialog);

// Let the user select multiple files
var files = FileDialog.openMulti();
if (files == null) throw "User cancelled!";

// Create detector
var detector = new UDWTWavelet();

// Iterate through selected files
for (var j = 0; j < files.length; ++j) {
    var f = files[j];
    println("Processing file: " + f.getName());

    // Create new Excel workbook for .xlsx
    var workbook = new XSSFWorkbook();
    var sheet = workbook.createSheet("Detection Results");

    // Create headers
    var headerRow = sheet.createRow(0);
    headerRow.createCell(0).setCellValue("File Name");
    headerRow.createCell(1).setCellValue("Time Frame");
    headerRow.createCell(2).setCellValue("Channel");
    headerRow.createCell(3).setCellValue("Detection Index");
    headerRow.createCell(4).setCellValue("X Coordinate");
    headerRow.createCell(5).setCellValue("Y Coordinate");
    headerRow.createCell(6).setCellValue("Average Intensity");

    // Variable for row index in Excel
    var rowIndex = 1;

    // Load sequence
    var sequence = Loader.loadSequence(f);
    if (sequence == null) {
        MessageDialog.showDialog("Unable to load sequence: " + f.getName(), MessageDialog.INFORMATION_MESSAGE);
        continue; // Skip file if loading sequence fails
    }

    sequence.removeAllROI(); // Clear existing ROIs
    var numChannels = sequence.getSizeC();
    println("Number of channels: " + numChannels);

    // Iterate through frames and channels
    for (var frameNumber = 0; frameNumber < sequence.getSizeT(); frameNumber++) {
        for (var channel = 0; channel < numChannels; channel++) {
            var image = sequence.getImage(frameNumber, channel); // Get image for channel
            if (image == null) {
                println("Skipping null image at frame " + frameNumber + ", channel " + channel);
                continue; // Skip processing if image is not available
            }

            println("Processing Time t=" + frameNumber + ", Channel=" + channel);
            var parameterForScale2 = 30 + frameNumber * 0.3;
            var scaleParameters = [0, parameterForScale2];

            println("Scale 2 parameter=" + parameterForScale2);

            var tmpSequence = new Sequence();
            tmpSequence.addImage(0, image);
            detector.detect(tmpSequence, false, false, scaleParameters);
            var detectionResult = detector.getDetectionResult();

            var detectionSize = detectionResult.size();
            println("Number of detections in channel " + channel + ": " + detectionSize);

            // Display results on the original sequence and filter by intensity
            var raster = image.getRaster(); // Access the image raster
            for (var i = 0; i < detectionSize; i++) {
                var spot = detectionResult.get(i);
                var massCenter = spot.getMassCenter();
                var x = massCenter.x;
                var y = massCenter.y;

                // Calculate average intensity around the spot
                var boxSize = 5; // Define a region size around the center
                var intensitySum = 0;
                var count = 0;

                for (var dx = -boxSize; dx <= boxSize; dx++) {
                    for (var dy = -boxSize; dy <= boxSize; dy++) {
                        var px = Math.round(x + dx);
                        var py = Math.round(y + dy);
                        if (px >= 0 && py >= 0 && px < image.getWidth() && py < image.getHeight()) {
                            intensitySum += raster.getSample(px, py, 0); // Get pixel intensity from the raster
                            count++;
                        }
                    }
                }

                var averageIntensity = intensitySum / count;

                // Filter spots based on intensity threshold
                if (averageIntensity > 100) { // Example threshold value
                    var roi = new ROI2DRectangle(
                        new Point2D.Double(x - boxSize, y - boxSize),
                        new Point2D.Double(x + boxSize + 1, y + boxSize + 1),
                        false
                    );
                    sequence.addROI(roi);

                    // Write data to Excel
                    var row = sheet.createRow(rowIndex++);
                    row.createCell(0).setCellValue(f.getName()); // File Name
                    row.createCell(1).setCellValue(frameNumber); // Time Frame
                    row.createCell(2).setCellValue(channel); // Channel
                    row.createCell(3).setCellValue(i);           // Detection Index
                    row.createCell(4).setCellValue(x);           // X Coordinate
                    row.createCell(5).setCellValue(y);           // Y Coordinate
                    row.createCell(6).setCellValue(averageIntensity); // Average Intensity
                }
            }
        }
    }

    // Save Excel file in .xlsx format
    var outputFile = new FileOutputStream(f.getName() + "_DetectionResults.xlsx"); // Save to .xlsx
    workbook.write(outputFile);
    outputFile.close();
    println("Results saved to " + f.getName() + "_DetectionResults.xlsx");
}
