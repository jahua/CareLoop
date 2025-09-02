Option Explicit

' ========= CONFIG =========
Private Const PROJECT_YEAR As Long = 2025
Private Const STEP_DAYS  As Long = 7
Private Const SHEET_NAME As String = "Paper_Timeline"

Private Function START_DATE() As Date: START_DATE = DateSerial(PROJECT_YEAR, 8, 25): End Function
Private Function END_DATE() As Date: END_DATE = DateSerial(PROJECT_YEAR, 12, 31): End Function

' ========= ENTRYPOINTS =========
Public Sub CreateCompletePaperTimeline()
    CreatePaperGanttChart
    AddMilestones
    AddKeyDeliverables
End Sub

Public Sub RebuildPaperTimeline()
    CreateCompletePaperTimeline
End Sub

' ========= DEBUG FUNCTIONS =========
Public Sub TestSheetCreation()
    Dim ws As Worksheet
    
    MsgBox "Testing sheet creation...", vbInformation, "Debug"
    
    On Error Resume Next
    Set ws = Worksheets.Add
    If Err.Number <> 0 Then
        MsgBox "Error adding sheet: " & Err.Description & " (Error " & Err.Number & ")", vbCritical, "Debug Error"
    Else
        MsgBox "Sheet added successfully!", vbInformation, "Debug Success"
        ws.Name = "TestSheet"
    End If
    On Error GoTo 0
End Sub

Public Sub CheckWorkbookStatus()
    Dim msg As String
    msg = "Workbook Info:" & vbCrLf
    msg = msg & "Active Workbook: " & ActiveWorkbook.Name & vbCrLf
    msg = msg & "Sheets Count: " & ActiveWorkbook.Sheets.Count & vbCrLf
    msg = msg & "Read Only: " & ActiveWorkbook.ReadOnly & vbCrLf
    msg = msg & "Saved: " & ActiveWorkbook.Saved & vbCrLf
    
    MsgBox msg, vbInformation, "Workbook Status"
End Sub

' ========= MAIN =========
Private Sub CreatePaperGanttChart()
    Dim ws As Worksheet

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    On Error Resume Next
    Worksheets(SHEET_NAME).Delete
    On Error GoTo 0
    Application.DisplayAlerts = True

    Set ws = Worksheets.Add
    ws.Name = SHEET_NAME

    SetupHeaders ws
    PopulateProjectData ws
    CreateDateColumns ws, START_DATE, END_DATE, STEP_DAYS
    AddGanttBars ws, START_DATE, STEP_DAYS
    FormatGanttChart ws
    AddLegend ws
    FinalFormatting ws

    Application.ScreenUpdating = True
    MsgBox "Paper Timeline Gantt Chart created successfully.", vbInformation, "Paper Development Timeline"
End Sub

' ========= HEADERS =========
Private Sub SetupHeaders(ws As Worksheet)
    With ws
        .Range("A1").Value = "Research Paper Development Timeline: Adaptive LLM-Based Chatbot with Personality-Aware Dialogue"
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 21
        .Range("A1").HorizontalAlignment = xlCenter

        .Range("A2").Value = "Timeline: " & Format$(START_DATE, "mmm d, yyyy") & " – " & Format$(END_DATE, "mmm d, yyyy")
        .Range("A3").Value = "Current Date: " & Format$(Date, "mmmm d, yyyy")
        .Range("A4").Value = "Building on Samuel's Work with Human Evaluation by Dr. Mirjam Stieger"

        .Range("A7").Resize(1, 7).Value = Array("Week", "Dates", "Phase", "Key Activities", "Status", "Progress", "Dr. Stieger Contact")
        .Range("A7:G7").Font.Bold = True
        .Range("A7:G7").Interior.Color = RGB(79, 129, 189)
        .Range("A7:G7").Font.Color = RGB(255, 255, 255)
        .Range("A7:G7").HorizontalAlignment = xlCenter
    End With
End Sub

' ========= DATA =========
Private Function TaskMatrix() As Variant
    Dim Y As Long: Y = PROJECT_YEAR
    Dim tasks() As Variant

    ReDim tasks(0 To 8, 0 To 5)

    ' W1-4 (Completed)
    tasks(0, 0) = "W1-4"
    tasks(0, 1) = DateSerial(Y, 7, 18)
    tasks(0, 2) = DateSerial(Y, 8, 24)
    tasks(0, 3) = "Samuel's Thesis Analysis"
    tasks(0, 4) = "• Thesis review & understanding • Key findings extraction • Gap identification"
    tasks(0, 5) = "Completed"

    ' W5-6 (Completed)
    tasks(1, 0) = "W5-6"
    tasks(1, 1) = DateSerial(Y, 8, 25)
    tasks(1, 2) = DateSerial(Y, 9, 7)
    tasks(1, 3) = "First Draft Creation"
    tasks(1, 4) = "• Paper structure development • Initial content writing • Samuel's work integration"
    tasks(1, 5) = "Completed"

    ' W7-8
    tasks(2, 0) = "W7-8"
    tasks(2, 1) = DateSerial(Y, 9, 8)
    tasks(2, 2) = DateSerial(Y, 9, 21)
    tasks(2, 3) = "Content Enhancement"
    tasks(2, 4) = "• Literature review expansion • Methodology improvement • Technical validation"
    tasks(2, 5) = "Sep 15-16: Initial consultation"

    ' W9-10
    tasks(3, 0) = "W9-10"
    tasks(3, 1) = DateSerial(Y, 9, 14)
    tasks(3, 2) = DateSerial(Y, 9, 27)
    tasks(3, 3) = "Preliminary Writing"
    tasks(3, 4) = "• Initial paper writing • Content development • Structure refinement"
    tasks(3, 5) = "Sep 20: Paper review"

    ' W11-12
    tasks(4, 0) = "W11-12"
    tasks(4, 1) = DateSerial(Y, 9, 28)
    tasks(4, 2) = DateSerial(Y, 10, 11)
    tasks(4, 3) = "Human Evaluation Design"
    tasks(4, 4) = "• Dr. Stieger consultation • Evaluation protocol design • Ethics application"
    tasks(4, 5) = "Oct 6: Protocol review"

    ' W13-14
    tasks(5, 0) = "W13-14"
    tasks(5, 1) = DateSerial(Y, 10, 12)
    tasks(5, 2) = DateSerial(Y, 10, 25)
    tasks(5, 3) = "Human Evaluation Execution"
    tasks(5, 4) = "• Participant recruitment • Data collection • Initial analysis"
    tasks(5, 5) = "Oct 20: Results review"

    ' W15-16
    tasks(6, 0) = "W15-16"
    tasks(6, 1) = DateSerial(Y, 10, 26)
    tasks(6, 2) = DateSerial(Y, 11, 8)
    tasks(6, 3) = "Results Integration"
    tasks(6, 4) = "• Evaluation results analysis • Paper content updates • Discussion enhancement"
    tasks(6, 5) = "Nov 3: Results review"

    ' W17-18
    tasks(7, 0) = "W17-18"
    tasks(7, 1) = DateSerial(Y, 11, 9)
    tasks(7, 2) = DateSerial(Y, 11, 22)
    tasks(7, 3) = "Paper Refinement"
    tasks(7, 4) = "• Content revision • Peer review integration • Quality assurance"
    tasks(7, 5) = "Nov 17: Peer review prep"

    ' W19-20
    tasks(8, 0) = "W19-20"
    tasks(8, 1) = DateSerial(Y, 11, 23)
    tasks(8, 2) = DateSerial(Y, 12, 31)
    tasks(8, 3) = "Final Polish & Submission"
    tasks(8, 4) = "• Final revisions • Submission preparation • Publication process"
    tasks(8, 5) = "Dec 1: Final review"

    TaskMatrix = tasks
End Function

Private Sub PopulateProjectData(ws As Worksheet)
    Dim tasks As Variant: tasks = TaskMatrix()
    Dim i As Long, r0 As Long
    Dim today As Date: today = Date

    r0 = 8
    For i = LBound(tasks, 1) To UBound(tasks, 1)
        Dim d0 As Date, d1 As Date
        d0 = tasks(i, 1): d1 = tasks(i, 2)

        ws.Cells(r0 + i, 1).Value = tasks(i, 0)
        ws.Cells(r0 + i, 2).Value = Format$(d0, "mmm d") & "–" & Format$(d1, "mmm d")
        ws.Cells(r0 + i, 3).Value = tasks(i, 3)
        ws.Cells(r0 + i, 4).Value = tasks(i, 4)
        ws.Cells(r0 + i, 5).Value = ComputeStatus(today, d0, d1)
        ws.Cells(r0 + i, 6).Value = ComputeProgressText(today, d0, d1)
        ws.Cells(r0 + i, 7).Value = tasks(i, 5)
        ws.Rows(r0 + i).RowHeight = 35
    Next i

    With ws.Range(ws.Cells(r0, 1), ws.Cells(r0 + UBound(tasks, 1), 7))
        .Borders.LineStyle = xlContinuous
        .Borders.Weight = xlThin
        .VerticalAlignment = xlTop
        .WrapText = True
    End With
End Sub

Private Function ComputeStatus(today As Date, d0 As Date, d1 As Date) As String
    If today < d0 Then
        ComputeStatus = "PLANNED"
    ElseIf today > d1 Then
        ComputeStatus = "COMPLETED"
    Else
        ComputeStatus = "IN PROGRESS"
    End If
End Function

Private Function ComputeProgressText(today As Date, d0 As Date, d1 As Date) As String
    Dim pct As Double, span As Long, doneDays As Long
    span = d1 - d0 + 1
    If today < d0 Then
        pct = 0
    ElseIf today > d1 Then
        pct = 1
    Else
        doneDays = today - d0 + 1
        pct = doneDays / span
    End If
    ComputeProgressText = CStr(Round(pct * 100, 0)) & "%"
End Function

' ========= DATE COLUMNS =========
Private Sub CreateDateColumns(ws As Worksheet, startDate As Date, endDate As Date, Optional stepDays As Long = 7)
    Dim d As Date, col As Long, weekStart As Date
    col = 8
    d = startDate

    Do While d <= endDate
        weekStart = d - (Weekday(d, vbMonday) - 1)
        ws.Cells(7, col).Value = Format$(weekStart, "dd-mmm")
        With ws.Cells(7, col)
            .Font.Bold = True
            .Interior.Color = RGB(219, 229, 241)
            .HorizontalAlignment = xlCenter
            .Orientation = 45
        End With
        ws.Columns(col).ColumnWidth = 8

        d = d + stepDays
        col = col + 1
    Loop
End Sub

' ========= GANTT BARS =========
Private Sub AddGanttBars(ws As Worksheet, startDate As Date, Optional stepDays As Long = 7)
    Dim tasks As Variant: tasks = TaskMatrix()
    Dim i As Long, r0 As Long, currentRow As Long
    Dim d0 As Date, d1 As Date
    Dim cStart As Long, cEnd As Long

    r0 = 8
    For i = LBound(tasks, 1) To UBound(tasks, 1)
        currentRow = r0 + i
        d0 = tasks(i, 1): d1 = tasks(i, 2)

        cStart = 8 + Int((d0 - startDate) / stepDays)
        cEnd = 8 + Int((d1 - startDate) / stepDays)
        If cStart < 8 Then cStart = 8
        If cEnd < cStart Then cEnd = cStart

        Dim fillColor As Long
        Select Case ComputeStatus(Date, d0, d1)
            Case "COMPLETED":   fillColor = RGB(34, 139, 34)
            Case "IN PROGRESS": fillColor = RGB(255, 165, 0)
            Case Else:          fillColor = RGB(169, 169, 169)
        End Select

        ws.Range(ws.Cells(currentRow, cStart), ws.Cells(currentRow, cEnd)).Interior.Color = fillColor
    Next i
End Sub

' ========= FORMATTING =========
Private Sub FormatGanttChart(ws As Worksheet)
    Dim lastRow As Long, i As Long
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row

    With ws
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 14
        .Columns("C").ColumnWidth = 25
        .Columns("D").ColumnWidth = 45
        .Columns("E").ColumnWidth = 16
        .Columns("F").ColumnWidth = 10
        .Columns("G").ColumnWidth = 25

        For i = 8 To lastRow
            Select Case UCase$(Trim$(.Range("E" & i).Value))
                Case "COMPLETED":   .Range("E" & i).Interior.Color = RGB(144, 238, 144)
                Case "IN PROGRESS": .Range("E" & i).Interior.Color = RGB(255, 215, 0)
                Case "PLANNED":     .Range("E" & i).Interior.Color = RGB(211, 211, 211)
                Case Else:          .Range("E" & i).Interior.ColorIndex = xlNone
            End Select

            .Range("F" & i).HorizontalAlignment = xlCenter
            If .Range("F" & i).Value = "100%" Then
                .Range("F" & i).Interior.Color = RGB(144, 238, 144)
            ElseIf .Range("F" & i).Value Like "*%" And .Range("F" & i).Value <> "0%" Then
                .Range("F" & i).Interior.Color = RGB(255, 215, 0)
            End If
        Next i
    End With
End Sub

' ========= LEGEND =========
Private Sub AddLegend(ws As Worksheet)
    Dim topRow As Long
    topRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row + 2

    With ws
        .Range("A" & topRow).Value = "LEGEND:"
        .Range("A" & topRow).Font.Bold = True

        .Cells(topRow + 1, 1).Interior.Color = RGB(34, 139, 34): .Cells(topRow + 1, 2).Value = "COMPLETED"
        .Cells(topRow + 2, 1).Interior.Color = RGB(255, 165, 0): .Cells(topRow + 2, 2).Value = "IN PROGRESS"
        .Cells(topRow + 3, 1).Interior.Color = RGB(169, 169, 169): .Cells(topRow + 3, 2).Value = "PLANNED"
    End With
End Sub

' ========= FINAL FORMATTING =========
Private Sub FinalFormatting(ws As Worksheet)
    Dim lastRow As Long, lastCol As Long
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    lastCol = ws.Cells(7, ws.Columns.Count).End(xlToLeft).Column

    With ws
        .Range("A7:G" & lastRow).Borders.LineStyle = xlContinuous
        .Range("A7:G" & lastRow).Borders.Weight = xlMedium
        If lastCol >= 8 Then
            .Range(.Cells(7, 8), .Cells(lastRow, lastCol)).Borders.LineStyle = xlThin
        End If

        With .Range(.Cells(1, 1), .Cells(1, lastCol))
            .Merge
            .Value = "Research Paper Development Timeline: Adaptive LLM-Based Chatbot with Personality-Aware Dialogue"
            .HorizontalAlignment = xlCenter
            .VerticalAlignment = xlCenter
            .Font.Bold = True
            .Font.Size = 21
            .Interior.Color = RGB(79, 129, 189)
            .Font.Color = RGB(255, 255, 255)
        End With
    End With
End Sub

' ========= MILESTONES =========
Public Sub AddMilestones()
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = Worksheets(SHEET_NAME)
    On Error GoTo 0
    If ws Is Nothing Then
        MsgBox "Sheet '" & SHEET_NAME & "' not found. Run CreateCompletePaperTimeline first.", vbExclamation
        Exit Sub
    End If

    Dim Y As Long: Y = PROJECT_YEAR
    Dim milestones As Variant
    Dim teamMeetings As Variant
    Dim expertConsultations As Variant
    
    ' Major Supervisor Meetings (Red)
    milestones = Array( _
        Array(DateSerial(Y, 9, 15), "Content Review", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 9, 29), "Evaluation Design", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 10, 13), "Evaluation Progress", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 10, 27), "Results Integration", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 11, 10), "Peer Review Prep", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 11, 24), "Final Review", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 12, 8), "Submission Review", RGB(255, 0, 0)) _
    )
    
    ' Team Meetings (Blue)
    teamMeetings = Array( _
        Array(DateSerial(Y, 9, 8), "Content Enhancement", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 9, 22), "Evaluation Planning", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 10, 6), "Evaluation Execution", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 10, 20), "Results Analysis", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 11, 3), "Paper Refinement", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 11, 17), "Final Polish", RGB(0, 0, 255)) _
    )
    
    ' Dr. Stieger Consultations (Green)
    expertConsultations = Array( _
        Array(DateSerial(Y, 9, 15), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 16), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 22), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 23), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 29), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 30), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 10, 13), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 10, 14), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 10, 27), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 10, 28), "Dr. Stieger", RGB(0, 128, 0)) _
    )

    Dim rowM As Long, i As Long, col As Long
    rowM = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row + 2
    
    ' Add Milestones Section
    ws.Range("A" & rowM).Value = "Major Milestones:"
    ws.Range("A" & rowM).Font.Bold = True
    ws.Range("A" & rowM).Font.Size = 14

    For i = LBound(milestones) To UBound(milestones)
        col = 8 + Int((milestones(i)(0) - START_DATE) / STEP_DAYS)
        ws.Cells(rowM, col).Value = "★"
        ws.Cells(rowM, col).Font.Color = milestones(i)(2)
        ws.Cells(rowM, col).Font.Size = 16
        ws.Cells(rowM, col).HorizontalAlignment = xlCenter

        ws.Cells(rowM + 1, col).Value = milestones(i)(1)
        ws.Cells(rowM + 1, col).Font.Size = 10
        ws.Cells(rowM + 1, col).HorizontalAlignment = xlCenter
        ws.Cells(rowM + 1, col).Font.Color = milestones(i)(2)
    Next i
    
    ' Add Team Meetings Section
    rowM = rowM + 3
    ws.Range("A" & rowM).Value = "Team Meetings:"
    ws.Range("A" & rowM).Font.Bold = True
    ws.Range("A" & rowM).Font.Size = 12

    For i = LBound(teamMeetings) To UBound(teamMeetings)
        col = 8 + Int((teamMeetings(i)(0) - START_DATE) / STEP_DAYS)
        ws.Cells(rowM, col).Value = "●"
        ws.Cells(rowM, col).Font.Color = teamMeetings(i)(2)
        ws.Cells(rowM, col).Font.Size = 14
        ws.Cells(rowM, col).HorizontalAlignment = xlCenter

        ws.Cells(rowM + 1, col).Value = teamMeetings(i)(1)
        ws.Cells(rowM + 1, col).Font.Size = 8
        ws.Cells(rowM + 1, col).HorizontalAlignment = xlCenter
        ws.Cells(rowM + 1, col).Font.Color = teamMeetings(i)(2)
    Next i
    
    ' Add Dr. Stieger Consultations Section
    rowM = rowM + 3
    ws.Range("A" & rowM).Value = "Dr. Stieger Consultations:"
    ws.Range("A" & rowM).Font.Bold = True
    ws.Range("A" & rowM).Font.Size = 12

    For i = LBound(expertConsultations) To UBound(expertConsultations)
        col = 8 + Int((expertConsultations(i)(0) - START_DATE) / STEP_DAYS)
        ws.Cells(rowM, col).Value = "◆"
        ws.Cells(rowM, col).Font.Color = expertConsultations(i)(2)
        ws.Cells(rowM, col).Font.Size = 12
        ws.Cells(rowM, col).HorizontalAlignment = xlCenter

        ws.Cells(rowM + 1, col).Value = expertConsultations(i)(1)
        ws.Cells(rowM + 1, col).Font.Size = 8
        ws.Cells(rowM + 1, col).HorizontalAlignment = xlCenter
        ws.Cells(rowM + 1, col).Font.Color = expertConsultations(i)(2)
    Next i
    
    ' Add Legend
    rowM = rowM + 3
    ws.Range("A" & rowM).Value = "Legend:"
    ws.Range("A" & rowM).Font.Bold = True
    ws.Range("A" & rowM).Font.Size = 12
    
    ws.Cells(rowM + 1, 1).Value = "★ Red = Supervisor Meetings"
    ws.Cells(rowM + 1, 1).Font.Color = RGB(255, 0, 0)
    ws.Cells(rowM + 2, 1).Value = "● Blue = Team Meetings (Duojie + Guang + Samuel)"
    ws.Cells(rowM + 2, 1).Font.Color = RGB(0, 0, 255)
    ws.Cells(rowM + 3, 1).Value = "◆ Green = Dr. Stieger Consultations"
    ws.Cells(rowM + 3, 1).Font.Color = RGB(0, 128, 0)
End Sub

Public Sub AddKeyDeliverables()
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = Worksheets(SHEET_NAME)
    On Error GoTo 0
    If ws Is Nothing Then
        MsgBox "Sheet '" & SHEET_NAME & "' not found. Run CreateCompletePaperTimeline first.", vbExclamation
        Exit Sub
    End If

    Dim Y As Long: Y = PROJECT_YEAR
    Dim deliverables As Variant
    Dim decisionPoints As Variant
    
    ' Key Deliverables (Purple)
    deliverables = Array( _
        Array(DateSerial(Y, 9, 21), "Enhanced Literature Review", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 9, 27), "Preliminary Paper Draft", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 10, 11), "Human Evaluation Protocol", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 10, 25), "Human Evaluation Results", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 11, 8), "Results Integration", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 11, 22), "Peer Review Version", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 12, 31), "Final Submission", RGB(128, 0, 128)) _
    )
    
    ' Critical Decision Points (Orange)
    decisionPoints = Array( _
        Array(DateSerial(Y, 9, 20), "Literature Review Complete", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 9, 26), "Preliminary Writing Complete", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 10, 10), "Evaluation Protocol Approved", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 10, 24), "Data Collection Complete", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 11, 7), "Results Integration Complete", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 11, 21), "Peer Review Ready", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 12, 30), "Final Submission Complete", RGB(255, 165, 0)) _
    )

    Dim rowD As Long, i As Long, col As Long
    rowD = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row + 2
    
    ' Add Deliverables Section
    ws.Range("A" & rowD).Value = "Key Deliverables:"
    ws.Range("A" & rowD).Font.Bold = True
    ws.Range("A" & rowD).Font.Size = 12

    For i = LBound(deliverables) To UBound(deliverables)
        col = 8 + Int((deliverables(i)(0) - START_DATE) / STEP_DAYS)
        ws.Cells(rowD, col).Value = "📄"
        ws.Cells(rowD, col).Font.Color = deliverables(i)(2)
        ws.Cells(rowD, col).Font.Size = 14
        ws.Cells(rowD, col).HorizontalAlignment = xlCenter

        ws.Cells(rowD + 1, col).Value = deliverables(i)(1)
        ws.Cells(rowD + 1, col).Font.Size = 8
        ws.Cells(rowD + 1, col).HorizontalAlignment = xlCenter
        ws.Cells(rowD + 1, col).Font.Color = deliverables(i)(2)
        ws.Cells(rowD + 1, col).WrapText = True
    Next i
    
    ' Add Decision Points Section
    rowD = rowD + 3
    ws.Range("A" & rowD).Value = "Critical Decisions:"
    ws.Range("A" & rowD).Font.Bold = True
    ws.Range("A" & rowD).Font.Size = 12

    For i = LBound(decisionPoints) To UBound(decisionPoints)
        col = 8 + Int((decisionPoints(i)(0) - START_DATE) / STEP_DAYS)
        ws.Cells(rowD, col).Value = "⚡"
        ws.Cells(rowD, col).Font.Color = decisionPoints(i)(2)
        ws.Cells(rowD, col).Font.Size = 14
        ws.Cells(rowD, col).HorizontalAlignment = xlCenter

        ws.Cells(rowD + 1, col).Value = decisionPoints(i)(1)
        ws.Cells(rowD + 1, col).Font.Size = 8
        ws.Cells(rowD + 1, col).HorizontalAlignment = xlCenter
        ws.Cells(rowD + 1, col).Font.Color = decisionPoints(i)(2)
        ws.Cells(rowD + 1, col).WrapText = True
    Next i
    
    ' Add to Legend
    rowD = rowD + 3
    ws.Cells(rowD, 1).Value = "📄 Purple = Key Deliverables"
    ws.Cells(rowD, 1).Font.Color = RGB(128, 0, 128)
    ws.Cells(rowD + 1, 1).Value = "⚡ Orange = Critical Decision Points"
    ws.Cells(rowD + 1, 1).Font.Color = RGB(255, 165, 0)
End Sub 