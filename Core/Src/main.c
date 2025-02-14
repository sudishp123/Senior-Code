/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define RX_BUFFER_SIZE 20
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

TIM_HandleTypeDef htim3;

UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
/* Frequency Variables */
float_t strain_rate; //Strain Rate Will be Pulled as an input through UART
float_t strain;
float_t length_specimen = 0.004; //Length of the Sample
float_t radius_specimen = 0.0015; //Radius of the Sample

//Variables Used to Calculate Speed from Strain Rater and then to create PWM Signals
uint16_t prescaler = 12; 
uint16_t steps_per = 1600;
uint16_t min_seconds = 60;
uint32_t clock_frequency = 16e6;
uint8_t duration = 50;
float_t speed;
uint16_t ARR;
uint16_t frequency;

//Variables for UART Communication
uint16_t lux = 0;
float_t angle;
char msg[100];
uint8_t rx_buffer[RX_BUFFER_SIZE];
uint8_t tx_buffer[50];
uint8_t rx_index = 0;

//Variable Changes when terminate test is clicked
volatile uint8_t stop_motor= 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_ADC1_Init(void);
static void MX_TIM3_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */
void Motor_Enable(uint8_t ena);
void Motor_SetPWM(void);
void Motor_SetDirection(uint8_t dir);
void Motor_RampUp(uint16_t maxFrequency, uint16_t duration);
uint16_t read_ADC(void);
float calculate_velocity(float dt);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();
  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_ADC1_Init();
  MX_TIM3_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */
  HAL_UART_Receive_IT(&huart2, &rx_buffer[rx_index], 1);
  HAL_UART_Transmit(&huart2, rx_buffer, strlen((char*)rx_buffer),HAL_MAX_DELAY);
  // 
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */
    if (strain_rate > 0)
        {
          Motor_Enable(1);
          Motor_SetDirection(1); // CW Direction
          if (strain_rate <= 13)
          {
            Motor_SetPWM();  
          }
          else
          {
          Motor_RampUp(frequency, duration);
          }
        }
        else
        {
        Motor_Enable(0); 
        HAL_TIM_PWM_Stop(&htim3, TIM_CHANNEL_1);
        }

    HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
    HAL_Delay(500);
    float sampling_frequency = (2e6)/(12.5+239.5);
    float dt= 1/(sampling_frequency);
    float velocity = calculate_velocity(dt);

    /* USER CODE BEGIN 3 */
    // HAL_ADC_Start(&hadc1);
    // HAL_ADC_PollForConversion(&hadc1,20);
    // lux = HAL_ADC_GetValue(&hadc1);
    // angle= ((float)lux/3072.0)*270;
    // sprintf(msg, "Velocity: %.2f m/s\r\n", velocity);
    // HAL_UART_Transmit(&huart2,(uint8_t *)msg,strlen(msg),HAL_MAX_DELAY);
    // HAL_Delay(500);
    if (stop_motor)
    {
      HAL_TIM_PWM_Stop(&htim3, TIM_CHANNEL_1);
      Motor_Enable(0);
      stop_motor = 0; 
    }
    HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
    HAL_Delay(500);
    } 
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI_DIV2;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV8;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Common config
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure Regular Channel
  */
  sConfig.Channel = ADC_CHANNEL_0;
  sConfig.Rank = ADC_REGULAR_RANK_1;
  sConfig.SamplingTime = ADC_SAMPLETIME_239CYCLES_5;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = prescaler-1;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = ARR-1;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = ARR/2;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */
  HAL_TIM_MspPostInit(&htim3);
}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, LD2_Pin|DIR_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(ENA_Pin_GPIO_Port, ENA_Pin_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LD2_Pin DIR_Pin */
  GPIO_InitStruct.Pin = LD2_Pin|DIR_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : ENA_Pin_Pin */
  GPIO_InitStruct.Pin = ENA_Pin_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ENA_Pin_GPIO_Port, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI15_10_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
/**
  * @brief Gradual ramp-up of motor speed to prevent stalling.
  * @param maxFrequency: Target frequency to achieve.
  * @param duration: Duration in seconds to maintain maximum speed.
  * @retval None
  */
void Motor_RampUp(uint16_t maxFrequency, uint16_t duration)
{
  uint16_t currentFrequency = 11000; // Starting frequency
  uint16_t step = 100;              // Increment frequency by this value
  uint16_t rampDelay = 1;        // Milliseconds delay between frequency increments

  while (currentFrequency < maxFrequency)
  {
    ARR = clock_frequency / (prescaler * currentFrequency);
    __HAL_TIM_SET_AUTORELOAD(&htim3, ARR - 1);
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, ARR / 2);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    currentFrequency += step;
    HAL_Delay(rampDelay);
  }
  __HAL_TIM_SET_AUTORELOAD(&htim3, ARR - 1);
  __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, ARR / 2);
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
  HAL_Delay(duration * 1000);
  HAL_TIM_PWM_Stop(&htim3, TIM_CHANNEL_1);
}

/**
  * @brief Motor Enable Function
  * @param ena
  * @retval None
  */
void Motor_Enable(uint8_t ena)
{
  if (ena)
  {
    HAL_GPIO_WritePin(ENA_Pin_GPIO_Port, ENA_Pin_Pin, GPIO_PIN_SET);
  }
  else
  {
    HAL_GPIO_WritePin(ENA_Pin_GPIO_Port, ENA_Pin_Pin, GPIO_PIN_RESET);
  }
}

/**
  * @brief Motor Direction Function
  * @param dir
  * @retval None
  */
void Motor_SetDirection(uint8_t dir)
{
  if (dir)
  {
    HAL_GPIO_WritePin(DIR_GPIO_Port, DIR_Pin, GPIO_PIN_SET);
  }
  else
  {
    HAL_GPIO_WritePin(DIR_GPIO_Port, DIR_Pin, GPIO_PIN_RESET);
  }
}

/**
  * @brief Motor Step Function
  * @param None
  * @retval None
  */
void Motor_SetPWM(void)
{
  __HAL_TIM_SET_AUTORELOAD(&htim3, ARR - 1);
  __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, ARR / 2);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    HAL_Delay(duration*1000);
    HAL_TIM_PWM_Stop(&htim3, TIM_CHANNEL_1);
}

uint16_t read_ADC(void){
  HAL_ADC_Start(&hadc1);
  HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
  return HAL_ADC_GetValue(&hadc1);
}

float_t calculate_velocity(float dt){
  static uint16_t prev_adc_value = 0;
  uint16_t current_adc_value = read_ADC();

  float theta_current = (current_adc_value/(float)4096)*360.0;
  float theta_previous = (prev_adc_value/(float)4096)*360.0;

  float delta_theta = theta_current - theta_previous;
  if (delta_theta > 180) delta_theta -=360;
  if (delta_theta < -180) delta_theta +=360;

  float omega = delta_theta/dt;
  return omega;

  prev_adc_value = current_adc_value;
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART2)
    {
        uint8_t received_char = rx_buffer[rx_index];

        if (received_char == 'S')
        {
          stop_motor=1;
        }

        else if (received_char == '\n' || rx_index >= RX_BUFFER_SIZE)
        {
          rx_buffer[rx_index] = '\0';
          HAL_UART_Transmit(&huart2, rx_buffer, rx_index, HAL_MAX_DELAY);

          char *token = strtok((char*)rx_buffer," ");
          if (token != NULL)
          {
            strain_rate= strtof(token, NULL);
            token= strtok(NULL, " ");
            if (token != NULL)
            {
              strain = strtof(token, NULL);
            }
          }
          speed = (sqrt(3) * strain_rate * length_specimen * min_seconds) / (2 * M_PI * radius_specimen);
          frequency = (speed * steps_per) / min_seconds;
          ARR = clock_frequency / (prescaler * frequency);  
          rx_index = 0; 
        }
        else
        {
          rx_index++;
        }
    }
    HAL_UART_Receive_IT(&huart2, &rx_buffer[rx_index], 1);
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */