Option Explicit

' ========= CONFIG =========
Private Const PROJECT_YEAR As Long = 2025   ' <<< set the project year here
Private Const STEP_DAYS  As Long = 7        ' 7 = weekly columns, 1 = daily
Private Const SHEET_NAME As String = "PMT"

Private Function START_DATE() As Date: START_DATE = DateSerial(PROJECT_YEAR, 7, 18): End Function
Private Function END_DATE() As Date:     END_DATE = DateSerial(PROJECT_YEAR, 10, 25): End Function


' ========= ENTRYPOINTS =========
Public Sub CreateCompletePMTGanttChart()
    CreatePMTGanttChart
    AddMilestones
    AddKeyDeliverables
End Sub

Public Sub RebuildPMT()
    CreateCompletePMTGanttChart
End Sub

Public Sub AddKeyDeliverables()
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = Worksheets(SHEET_NAME)
    On Error GoTo 0
    If ws Is Nothing Then
        MsgBox "Sheet '" & SHEET_NAME & "' not found. Run CreateCompletePMTGanttChart first.", vbExclamation
        Exit Sub
    End If

    Dim Y As Long: Y = PROJECT_YEAR
    Dim deliverables As Variant
    Dim decisionPoints As Variant
    
    ' Key Deliverables (Purple)
    deliverables = Array( _
        Array(DateSerial(Y, 8, 30), "Tech Framework Proposal", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 9, 6), "Technical Specs Document", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 9, 13), "Implementation Plan", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 9, 20), "Research Paper (90%)", RGB(128, 0, 128)), _
        Array(DateSerial(Y, 9, 27), "PMT Report & Presentation", RGB(128, 0, 128)) _
    )
    
    ' Critical Decision Points (Orange)
    decisionPoints = Array( _
        Array(DateSerial(Y, 8, 28), "Framework Selection", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 9, 5), "Architecture Finalization", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 9, 12), "User Study Protocol", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 9, 19), "Paper Structure", RGB(255, 165, 0)), _
        Array(DateSerial(Y, 9, 26), "Final Submission", RGB(255, 165, 0)) _
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


' ========= MAIN =========
Private Sub CreatePMTGanttChart()
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
    MsgBox "Gantt Chart (PMT) created successfully.", vbInformation, "Project Timeline"
End Sub


' ========= HEADERS =========
Private Sub SetupHeaders(ws As Worksheet)
    With ws
        .Range("A1").Value = "Adaptive LLM-based Chatbot Project Preliminary Study Timeline"
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 21
        .Range("A1").HorizontalAlignment = xlCenter

        .Range("A2").Value = "Timeline: " & Format$(START_DATE, "mmm d, yyyy") & " – " & Format$(END_DATE, "mmm d, yyyy")
        .Range("A3").Value = "Current Date: " & Format$(Date, "mmmm d, yyyy")

        .Range("A6").Resize(1, 7).Value = Array("Week", "Dates", "Phase", "Key Activities", "Status", "Progress", "Supervisor Meeting")
        .Range("A6:G6").Font.Bold = True
        .Range("A6:G6").Interior.Color = RGB(79, 129, 189)
        .Range("A6:G6").Font.Color = RGB(255, 255, 255)
        .Range("A6:G6").HorizontalAlignment = xlCenter
    End With
End Sub


' ========= DATA =========
Private Function TaskMatrix() As Variant
    Dim Y As Long: Y = PROJECT_YEAR
    Dim tasks() As Variant

    ReDim tasks(0 To 11, 0 To 5)

    ' W1
    tasks(0, 0) = "W1"
    tasks(0, 1) = DateSerial(Y, 7, 18)
    tasks(0, 2) = DateSerial(Y, 7, 26)
    tasks(0, 3) = "Foundation Setup"
    tasks(0, 4) = "• Kick-off meeting • Project scope • Team roles"
    tasks(0, 5) = "Jul 18: 1h kick-off, online meeting"

    ' W2-3
    tasks(1, 0) = "W2-3"
    tasks(1, 1) = DateSerial(Y, 7, 27)
    tasks(1, 2) = DateSerial(Y, 8, 9)
    tasks(1, 3) = "Samuel's Work Analysis"
    tasks(1, 4) = "• Thesis review • Technical study • Gap analysis"
    tasks(1, 5) = "-"

    ' W4-5
    tasks(2, 0) = "W4-5"
    tasks(2, 1) = DateSerial(Y, 8, 10)
    tasks(2, 2) = DateSerial(Y, 8, 16)
    tasks(2, 3) = "Literature Review"
    tasks(2, 4) = "• Psychology integration • Framework research"
    tasks(2, 5) = "-"

    ' W6-7
    tasks(3, 0) = "W6-7"
    tasks(3, 1) = DateSerial(Y, 8, 17)
    tasks(3, 2) = DateSerial(Y, 8, 23)
    tasks(3, 3) = "Team Discussion"
    tasks(3, 4) = "• Zurich Model Framework • Ethics"
    tasks(3, 5) = "Aug 18: Team sync, online meeting"

         ' W8
     tasks(4, 0) = "W8"
     tasks(4, 1) = DateSerial(Y, 8, 24)
     tasks(4, 2) = DateSerial(Y, 8, 30)
     tasks(4, 3) = "Technical Framework"
     tasks(4, 4) = "• Chatbot framework selection • Architecture planning"
     tasks(4, 5) = "Aug 30: Tech review"

     ' W9
     tasks(5, 0) = "W9"
     tasks(5, 1) = DateSerial(Y, 8, 31)
     tasks(5, 2) = DateSerial(Y, 9, 6)
     tasks(5, 3) = "Technical Specifications"
     tasks(5, 4) = "• Development timeline • User study design"
     tasks(5, 5) = "Sep 6: Spec review"

     ' W10
     tasks(6, 0) = "W10"
     tasks(6, 1) = DateSerial(Y, 9, 7)
     tasks(6, 2) = DateSerial(Y, 9, 13)
     tasks(6, 3) = "Implementation Planning"
     tasks(6, 4) = "• Testing strategy • Risk assessment"
     tasks(6, 5) = "Sep 13: Plan review"

     ' W11-12
     tasks(7, 0) = "W11-12"
     tasks(7, 1) = DateSerial(Y, 9, 14)
     tasks(7, 2) = DateSerial(Y, 9, 27)
     tasks(7, 3) = "Paper Writing"
     tasks(7, 4) = "• Research paper • Technical validation"
     tasks(7, 5) = "Sep 20: Paper review"

    ' W13
    tasks(8, 0) = "W13"
    tasks(8, 1) = DateSerial(Y, 9, 28)
    tasks(8, 2) = DateSerial(Y, 10, 4)
    tasks(8, 3) = "Final Delivery"
    tasks(8, 4) = "• PMT report • Final presentation"
    tasks(8, 5) = "Sep 27: Final review"

    ' W14
    tasks(9, 0) = "W14"
    tasks(9, 1) = DateSerial(Y, 10, 5)
    tasks(9, 2) = DateSerial(Y, 10, 11)
    tasks(9, 3) = "Buffer/Contingency"
    tasks(9, 4) = "• Polish • Contingency tasks"
    tasks(9, 5) = "-"

    ' W15
    tasks(10, 0) = "W15"
    tasks(10, 1) = DateSerial(Y, 10, 12)
    tasks(10, 2) = DateSerial(Y, 10, 18)
    tasks(10, 3) = "Buffer/Contingency"
    tasks(10, 4) = "• Polish • Contingency tasks"
    tasks(10, 5) = "-"

    ' W16
    tasks(11, 0) = "W16"
    tasks(11, 1) = DateSerial(Y, 10, 19)
    tasks(11, 2) = DateSerial(Y, 10, 25)
    tasks(11, 3) = "Wrap-up"
    tasks(11, 4) = "• Archive • Lessons learned"
    tasks(11, 5) = "-"

    TaskMatrix = tasks
End Function

Private Sub PopulateProjectData(ws As Worksheet)
    Dim tasks As Variant: tasks = TaskMatrix()
    Dim i As Long, r0 As Long
    Dim today As Date: today = Date

    r0 = 7
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
        ws.Rows(r0 + i).RowHeight = 30
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
        ws.Cells(6, col).Value = Format$(weekStart, "dd-mmm")
        With ws.Cells(6, col)
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

    r0 = 7
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
        .Columns("C").ColumnWidth = 22
        .Columns("D").ColumnWidth = 40
        .Columns("E").ColumnWidth = 16
        .Columns("F").ColumnWidth = 10
        .Columns("G").ColumnWidth = 20

        For i = 7 To lastRow
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
    lastCol = ws.Cells(6, ws.Columns.Count).End(xlToLeft).Column

    With ws
        .Range("A6:G" & lastRow).Borders.LineStyle = xlContinuous
        .Range("A6:G" & lastRow).Borders.Weight = xlMedium
        If lastCol >= 8 Then
            .Range(.Cells(6, 8), .Cells(lastRow, lastCol)).Borders.LineStyle = xlThin
        End If

        With .Range(.Cells(1, 1), .Cells(1, lastCol))
            .Merge
            .Value = "Adaptive LLM-based Chatbot Project Preliminary Study Timeline"
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
        MsgBox "Sheet '" & SHEET_NAME & "' not found. Run CreateCompletePMTGanttChart first.", vbExclamation
        Exit Sub
    End If

    Dim Y As Long: Y = PROJECT_YEAR
    Dim milestones As Variant
    Dim teamMeetings As Variant
    Dim expertConsultations As Variant
    
    ' Major Supervisor Meetings (Red)
    milestones = Array( _
        Array(DateSerial(Y, 8, 30), "Tech Review", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 9, 6), "Spec Review", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 9, 13), "Plan Review", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 9, 20), "Paper Review", RGB(255, 0, 0)), _
        Array(DateSerial(Y, 9, 27), "Final Review", RGB(255, 0, 0)) _
    )
    
    ' Team Meetings (Blue)
    teamMeetings = Array( _
        Array(DateSerial(Y, 8, 26), "Team Check-in", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 9, 2), "Specs Review", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 9, 9), "Implementation", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 9, 16), "Paper Support", RGB(0, 0, 255)), _
        Array(DateSerial(Y, 9, 23), "Final Prep", RGB(0, 0, 255)) _
    )
    
    ' Expert Consultations (Green)
    expertConsultations = Array( _
        Array(DateSerial(Y, 8, 27), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 8, 28), "Dr. Stieger", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 3), "Tech Expert", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 4), "Tech Expert", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 10), "User Study Expert", RGB(0, 128, 0)), _
        Array(DateSerial(Y, 9, 11), "User Study Expert", RGB(0, 128, 0)) _
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
    
    ' Add Expert Consultations Section
    rowM = rowM + 3
    ws.Range("A" & rowM).Value = "Expert Consultations:"
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
    ws.Cells(rowM + 3, 1).Value = "◆ Green = Expert Consultations"
    ws.Cells(rowM + 3, 1).Font.Color = RGB(0, 128, 0)
End Sub

