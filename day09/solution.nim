import std/[strutils, sequtils, algorithm, tables]

proc parseDisk(line: string): seq[int] =
  var disk: seq[int] = @[]
  var isFile = true
  var currentFileId = 0

  for c in line:
    let length = c.ord - '0'.ord
    if length < 0 or length > 9:
      raise newException(ValueError, "Invalid input character: " & c)

    if isFile:
      # Each file length digit, even if zero, defines a new file ID
      for _ in 0..<length:
        disk.add(currentFileId)
      currentFileId += 1
    else:
      for _ in 0..<length:
        disk.add(-1)
    isFile = not isFile

  return disk

proc findFreeSpans(disk: seq[int]): seq[(int, int)] =
  var spans: seq[(int, int)] = @[]
  var start = -1

  for i, diskSegment in disk:
    if diskSegment == -1:
      if start == -1:
        start = i
    else:
      if start != -1:
        spans.add((start, i - start))
        start = -1
  if start != -1:
    spans.add((start, disk.len - start))

  return spans

proc compactFiles(disk: var seq[int]) =
  # Identify unique files and their positions
  var fileIds: seq[int] = @[]
  var filePositions: Table[int, seq[int]] = initTable[int, seq[int]]()

  for i, diskSegment in disk:
    if diskSegment != -1:
      if diskSegment notin fileIds:
        fileIds.add(diskSegment)
        filePositions[diskSegment] = @[]
      filePositions[diskSegment].add(i)

  fileIds.sort()
  fileIds.reverse() # highest ID first

  for fileId in fileIds:
    let fileLength = filePositions[fileId].len
    if fileLength == 0:
      # This file might be zero-length; continue if needed
      continue

    # Determine the leftmost position of this file
    let minPos = filePositions[fileId].min

    # Find free spans
    var freeSpans = findFreeSpans(disk)

    # Filter free spans to only those fully to the left of minPos
    # i.e., freeSpan.start + freeSpan.length won't matter as long as start < minPos
    # The requirement doesn't say the entire file must fit strictly before minPos, only that
    # the free span is "to the left" of the file. The simplest interpretation is that the starting
    # position of the free span must be strictly less than minPos.
    freeSpans = freeSpans.filterIt(it[0] < minPos)

    # Now, pick the leftmost suitable span that can fit the file
    # freeSpans are returned left-to-right by findFreeSpans, so the first suitable is the leftmost.
    var moved = false
    for (start, length) in freeSpans:
      if length >= fileLength:
        # Move the file here
        # First, write the file blocks to the new location
        for j in 0..<fileLength:
          disk[start + j] = fileId

        # Clear old positions
        for pos in filePositions[fileId]:
          if pos < start or pos >= start + fileLength:
            disk[pos] = -1

        # Update stored positions
        filePositions[fileId] = @[]
        for j in 0..<fileLength:
          filePositions[fileId].add(start + j)

        moved = true
        break
    # If no suitable left free span found, file stays in place

proc computeChecksum(disk: seq[int]): int =
  var checksum = 0
  for i, diskSegment in disk:
    if diskSegment != -1:
      checksum += i * diskSegment
  return checksum

when isMainModule:
  let line = readFile("input.txt").strip()
  var disk = parseDisk(line)
  compactFiles(disk)
  let result = computeChecksum(disk)
  echo result
