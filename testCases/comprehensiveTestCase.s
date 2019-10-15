L1: add	$t1, $t2, $t3
	addu	$t1, $t2, $t3
	and	$s1, $s2, $s3
	nor	$a0, $a1, $a2
	or	$v1, $s1, $t1
	slt	$s4, $s5, $s6
	sltu	$t4, $t5, $t6
	sub	$v0, $a0, $t0
	subu	$a1, $a2, $a3
	lw	$t1, 4($t0)
	lw	$t2, -100($t0)
	sw	$t1, 4($t0)
	sw	$t2, -100($t0)
	beq	$t1, $t2, L2
	lw	$t2, 4($s0)
	lw	$t2, -8($s0)
	sw	$t1, 5293($s1)
	sw	$t1, -5293($s1)
	bne	$t1, $t2, L1
L2: sll	$s0, $s1, 2
	srl	$s1, $s0, 4
	andi	$t7, $t8, 256 
	ori	$t8, $t7, 3916
	addi	$t8, $t7, 3916
	beq	$t1, $t2, L1
    addiu $s6, $zero 5
    mult $v0, $a1
    div $t8, $t9
    multu $a1, $a2
    divu $a3, $t0
    mfhi $t1
    mflo $t2
    xor $t3, $t4, $t5
    xori $t6, $t7, 5
    sra $t8, $t9, 9
    sllv $s0, $s1, $s3
    srlv $s4, $s5, $s6
    srav $s7, $sp, $fp
    slti $t0, $s0, -5
    slti $a0, $s4, 5
    lui $a1, 1
    lb $s0, 8($s1)
    lbu $s0, 8($s1)
    lh $s0, 8($s1)
    lhu $s0, 8($s1)
    sb $s0, 8($s1)
    sh $s0, 8($s1)
    ll $s0, 8($s1)
    sc $s0, 8($s1)
