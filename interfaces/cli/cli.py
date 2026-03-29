import argparse
import sys
from application.use_cases.full_pipeline import TranscriptionPipeline

def main():
    parser = argparse.ArgumentParser(description="Desktop Transcription MVP System.")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: record-mic
    mic_parser = subparsers.add_parser("record-mic", help="Record from microphone and process")
    
    # Command: record-system
    sys_parser = subparsers.add_parser("record-system", help="Record system audio and process")
    
    # Command: process
    proc_parser = subparsers.add_parser("process", help="Process an existing audio/video file")
    proc_parser.add_argument("--file", required=True, help="Path to input file")

    # Command: full-run
    full_parser = subparsers.add_parser("full-run", help="Run full pipeline")
    full_parser.add_argument("--input", choices=["mic", "system"], help="Input mode")
    full_parser.add_argument("--file", help="Path to input file (if input is not mic or system)")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    pipeline = TranscriptionPipeline()

    if args.command == "record-mic":
        pipeline.record_microphone()
        
    elif args.command == "record-system":
        pipeline.record_system()
        
    elif args.command == "process":
        pipeline.process_file(args.file)
        
    elif args.command == "full-run":
        if args.input == "mic":
            pipeline.record_microphone()
        elif args.input == "system":
            pipeline.record_system()
        elif args.file:
            pipeline.process_file(args.file)
        else:
            print("Error: full-run requires --input or --file")
            sys.exit(1)

if __name__ == "__main__":
    main()
