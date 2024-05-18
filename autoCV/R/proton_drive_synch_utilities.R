sync_files_2_remote <- function(local_dir, remote_name, dry_run = FALSE){
  
  # write a cmd command using r clone that syncs files to a remote directory like rclone sync /home/source remote:backup
  cmd <- paste("rclone sync", local_dir, remote_name, "--progress")
  
  # add the dry run flag
  if(dry_run){
    cmd <- paste(cmd, "--dry-run")
  }
  
  # run the command
  system(cmd)
  
}


list_files_in_remote <- function(remote_name){
  
  # write a cmd command using r clone that lists files in path like rclone lsd Dar4Proton:  where Dar4Proton is the remote_name
  cmd <- paste("rclone lsd", remote_name)
  
  # run the command
  system(cmd)
}

synch_local_2_remote <- function(dryrun){
  
  sync_files_2_remote("'autoCV/cv types/'", "'Dar4Proton:Hot Bench Curriculum/'", dryrun)
  
}

# To copy a local file to an Proton Drive directory called backup
copy_file_2_remote <- function(local_file, remote_name, remote_dir){
  
  # write a cmd command using r clone that copies a file to a remote directory like rclone copy /home/source remote:backup
  cmd <- paste("rclone copy", local_file, remote_name, remote_dir)
  
  # run the command
  system(cmd)
  
}