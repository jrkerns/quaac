========
Examples
========

The following examples flesh out this abstract description:

* **CatPhan Measurement** - A therapist sets up a CatPhan on a linear accelerator (linac)
  couch and performs a cone-beam CT. The linac generates a set of DICOM files containing
  the measurement data. The DICOM files are sent to an image analysis software package.
  The user then records 5 uniformity measurements of the analysis in a spreadsheet. Later on, a physicist
  reviews the data and the spreadsheet to ensure that the analysis was performed correctly
  and marks the data as reviewed.

  In this case, the linac, the CatPhan, and the image analysis software could all be considered
  "equipment". The DICOM files and the spreadsheet are both "files". The data points are the
  outputs from the image analysis software and the spreadsheet. The therapist and physicist are
  both users. In this case we have:

  - 3 pieces of equipment (linac, CatPhan, image analysis software)
  - 2 files (DICOM set and spreadsheet)
  - 2 users (therapist and physicist)
  - 5 data points (the 5 uniformity measurements)

* **Monthly Output Checks** - Physicist A sets up solid water and an ion chamber and electrometer on a linac
  couch and performs a monthly dose output check. The charge from the ion chamber is recorded by the
  electrometer and the physicist records the data in a spreadsheet. This measurement is converted to dose
  and compared to the nominal value. Later on, physicist B
  reviews the data and the spreadsheet to ensure that the analysis was performed correctly and marks
  the data as reviewed. In this case we have:

  - 3 pieces of equipment (linac, solid water, ion chamber)
  - 1 file (spreadsheet)
  - 2 users (physicist A and physicist B)
  - 2+ data points (ion chamber reading, dose, and possibly intermediate calculations)

* **CT daily checkout** - A therapist sets up a manufacturer's phantom on a CT scanner and
  performs the pre-programmed daily check-out routine. The CT scanner analyzes the data and
  generates a PDF report that is saved to a network share. The therapist briefly looks at the
  PDF to ensure a "Pass" signal is given. Later on, a physicist looks at the
  PDF and records the "Pass" signal in a Word document along with the date of measurement.
  In this case we have:

  - 2 pieces of equipment (CT scanner and manufacturer's phantom)
  - 2 file (PDF report, Word document)
  - 2 users (therapist and physicist)
  - 1 data point (the "Pass" signal)

This should give an idea of the types of data acquired during routine QA and is the target of the QuAAC specification.
