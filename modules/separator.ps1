$from = $args[0]
$rootName = "$from"
$ext = "json"
$upperBound = 50MB

$fromFile = [io.file]::OpenRead($from)
$buff = new-object byte[] $upperBound
$count = $idx = 0
try {
    do {
        $count = $fromFile.Read($buff, 0, $buff.Length)
        if ($count -gt 0) {
            $to = "{0}_{1}" -f ($rootName, $idx)
            $toFile = [io.file]::OpenWrite($to)
            try {
                $tofile.Write($buff, 0, $count)
            } finally {
                $tofile.Close()
            }
        }
        $idx ++
    } while ($count -gt 0)
}
finally {
    $fromFile.Close()
    $idx--
    "Separated to $idx files"
}