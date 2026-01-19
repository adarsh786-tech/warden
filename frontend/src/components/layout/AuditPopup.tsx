import { useState } from "react";

import { Button } from "../ui/Button";
import { Label } from "../ui/Label";
import {
  Dialog,
  DialogTitle,
  DialogTrigger,
  DialogContent,
  DialogHeader,
} from "../ui/Dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/Select";
import { toast } from "sonner";
import { Separator } from "../ui/Separator";
import { FileText, Upload, PlayCircle } from "lucide-react";
import { extensions } from "../../data/acceptedExtensions";

const AuditPopup = () => {
  const [open, setOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileType, setFileType] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSubmit = () => {
    if (!selectedFile) {
      toast.error("No file selected", {
        description: "Please upload a file before submitting.",
      });
      return;
    }

    if (!fileType) {
      toast.error("No file type selected", {
        description: "Please select a file type.",
      });
      return;
    }

    toast.success("Submitted successfully!", {
      description: `File: ${selectedFile.name}, Type: ${fileType}`,
    });

    // Reset and close
    setSelectedFile(null);
    setFileType("");
    setOpen(false);
  };

  const handleOpenChange = (isOpen: boolean) => {
    setOpen(isOpen);
    if (!isOpen) {
      setSelectedFile(null);
      setFileType("");
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button className="gap-2 cursor-pointer">
          <PlayCircle className="h-4 w-4" />
          Run New Audit
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md shadow-xl bg-card border-border">
        <DialogHeader>
          <DialogTitle className="text-xl font-semibold text-card-foreground">
            Upload & Configure
          </DialogTitle>
        </DialogHeader>

        {/* Part 1: File Upload & Type Selection */}
        <div className="space-y-5">
          <div className="space-y-2">
            <Label
              htmlFor="file-upload"
              className="text-sm font-medium text-muted-foreground"
            >
              Upload File
            </Label>
            <div className="relative">
              <input
                id="file-upload"
                type="file"
                onChange={handleFileChange}
                className="hidden"
              />
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center justify-center w-full h-28 border-2 border-dashed border-border rounded-xl cursor-pointer bg-secondary/40 hover:bg-secondary/60 transition-all duration-200"
              >
                {selectedFile ? (
                  <div className="flex items-center gap-3 text-card-foreground">
                    <FileText className="h-7 w-7 text-primary" />
                    <span className="text-sm font-medium truncate max-w-50">
                      {selectedFile.name}
                    </span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-2 text-muted-foreground">
                    <Upload className="h-7 w-7" />
                    <span className="text-sm">Click to upload a file</span>
                  </div>
                )}
              </label>
            </div>
          </div>

          <div className="space-y-2">
            <Label
              htmlFor="file-type"
              className="text-sm font-medium text-muted-foreground"
            >
              File Type
            </Label>
            <Select value={fileType} onValueChange={setFileType}>
              <SelectTrigger
                id="file-type"
                className="w-full bg-secondary/30 border-border"
              >
                <SelectValue placeholder="Select file type" />
              </SelectTrigger>
              <SelectContent className="bg-popover border-border">
                {extensions.map((extension) => (
                  <SelectItem key={extension.id} value={extension.name}>
                    {extension.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator className="my-3 bg-border" />

        <Button onClick={handleSubmit} className="w-full mt-4 shadow-md">
          Submit
        </Button>
      </DialogContent>
    </Dialog>
  );
};

export default AuditPopup;
