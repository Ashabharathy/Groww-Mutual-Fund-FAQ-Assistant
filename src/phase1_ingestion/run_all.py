import asyncio
import subphase1_2_extract
import subphase1_3_clean_chunk
import subphase1_4_tag_export

def main():
    print("=========================================")
    print("  PHASE 1: DATA ACQUISITION & PREPARATION  ")
    print("=========================================\n")
    
    # Run Subphase 1.2 (1.1 is just the config file loaded by 1.2)
    asyncio.run(subphase1_2_extract.extract_all())
    
    # Run Subphase 1.3
    subphase1_3_clean_chunk.clean_and_chunk_all()
    
    # Run Subphase 1.4
    subphase1_4_tag_export.tag_and_export()
    
    print("=========================================")
    print("  PHASE 1 COMPLETED SUCCESSFULLY         ")
    print("=========================================")

if __name__ == "__main__":
    main()
